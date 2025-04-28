from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from datetime import date as date_, datetime
from typing import Optional
from openai import OpenAI
import json

from app.db.db import get_session
from app.models.gpt import GPTRecommendation
from app.models.gptDTO import GPTRequest
from app.models.gptDTO import GPTRecommendationResponse
from app.services.gpt_service import GPTService
from app.core.config import settings

router = APIRouter()

client = OpenAI(api_key=settings.OPENAI_KEY)

@router.post(
  "/recommend",
  response_model=dict,
  summary="GPT 식단/운동 추천 요청",
  description="유저 정보 기반으로 GPT에게 식단/운동 추천을 요청하고, DB에 저장 또는 업데이트합니다.",
  tags=["gpt"]
)
async def generate_recommendation(
  data: GPTRequest,
  session: AsyncSession = Depends(get_session)
):
  try:
    # 프롬프트 구성
    system_prompt = """
      당신은 맞춤형 식단 및 운동 계획을 제공하는 AI입니다. 사용자가 입력한 정보를 바탕으로 7일치 식단과 운동량을 구성하여 JSON 형식으로 출력하세요.
      
      [1] 식단 구성 조건:
      - 하루 총 섭취 칼로리는 '목표 칼로리' ±50kcal 이내
      - 아침/점심/저녁 구성, 각 끼니에 kcal 명시
      - '식단 타입'을 반영 (예: 고단백, 키토 등)
      - 알레르기 식품은 반드시 제외, 유사어 포함 금지

      - ⚠️ **중요**: 1인 가구 기준, 자취생이 혼자 준비할 수 있는 현실적인 식단이어야 함.
          - ✅ 냉동 식품, 즉석밥, 시판 샐러드, 전자레인지 조리 OK
          - ✅ 간단한 프라이팬 조리 정도는 허용
          - ❌ 오븐, 수비드, 장시간 조리, 복잡한 재료 손질 금지
          - ❌ '연어 스테이크', '해물찜', '오븐구이' 등은 제외
          - ❌ 재료 손질·조리가 복잡한 메뉴는 절대 포함하지 마세요

      - ⚠️ **질리지 않게** 구성: 맛/재료/조리법을 매일 다르게

      [2] 운동 구성 조건:
      - 사용자 정보 기반으로 '하루 목표 빠른 걸음 수' 계산
      - 1보당 0.04kcal 공식 사용 → 예: 10000보(400kcal)

      [3] 출력 예시 (반드시 JSON만 출력):
      { "식단": { "1일": { "아침": "...(kcal)", "점심": "...(kcal)", "저녁": "...(kcal)" }, ... }, "운동": { "하루 목표 빠른 걸음 수": 숫자(예상 소모 칼로리) (예: 10000(350kcal)) } }

      [주의사항]
      - 반드시 위 예시 구조 그대로 7일치 식단과 운동을 JSON 형식으로 출력하세요
      - 추가 설명, 주석, 줄바꿈 문자 (`\\n`, `\\`, ```json 등)는 절대 포함하지 마세요.
      - 모든 값은 반드시 문자열로 출력하세요. 예: "10000(400kcal)"
      - 출력 JSON은 유효한 구조여야 하며 쉼표, 따옴표 오류 없어야 함.
    """

    user_prompt = f"""
      나이: {data.age}세
      성별: {data.gender}
      키: {data.height}cm
      평소 활동량: {data.activity_level}
      현재 체중: {data.current_weight}kg
      목표 체중: {data.target_weight}kg
      목표 달성일: {data.target_date}
      목표 하루 섭취 칼로리: {data.target_calories}kcal
      감량 강도: {data.diet_intensity}
      식단 타입: {data.diet_type}
      식습관: {data.diet_type}
      알레르기: {', '.join(data.allergy)}
    """

    # GPT 호출
    response = client.chat.completions.create(
      model="gpt-4-turbo",
      messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
      ],
      temperature=0.5
    )

    result = response.choices[0].message.content
    print(f"📦 GPT 응답: {result}")

    # DB 저장
    gpt_service = GPTService(db=session)
    status = await gpt_service.create_or_update_recommendation(data.email, result)

    return {"message": f"추천 결과 {status} 완료", "recommendation": json.loads(result)}

  except Exception as e:
    print("🔥 GPT 추천 실패:", str(e))
    raise HTTPException(status_code=500, detail="GPT 추천 생성 실패")

@router.get(
  "/recommend",
  response_model=GPTRecommendationResponse,
  summary="저장된 GPT 추천 결과 조회",
  description="email과 date를 쿼리로 받아, 해당 날짜(혹은 그 이전) 가장 최신 저장된 추천을 반환합니다."
)
async def get_recommendation(
  email: str = Query(..., description="조회할 사용자 이메일"),
  date: Optional[date_] = Query(None, description="조회 기준 날짜 (YYYY-MM-DD). 미지정 시 오늘 기준)"),
  session: AsyncSession = Depends(get_session)
):
  # 1) 조회 기준 날짜 결정
  target: date_ = date or date_.today()

  # 2) email, created_at <= target 조건으로 가장 최신 한 건 선택
  stmt = (
    select(GPTRecommendation)
    .where(
      and_(
        GPTRecommendation.email == email,
        func.date(GPTRecommendation.created_at) <= target
      )
    )
    .order_by(GPTRecommendation.created_at.desc())
    .limit(1)
  )

  result = await session.execute(stmt)
  rec: GPTRecommendation = result.scalars().first()

  if not rec:
    raise HTTPException(status_code=404, detail="해당 날짜 기준 저장된 추천 결과가 없습니다.")
  
  # 3) Pydantic 응답 모델에 맞춰 반환
  return GPTRecommendationResponse(
    email=rec.email,
    recommendations=rec.recommendations,
    created_at=rec.created_at
  )
