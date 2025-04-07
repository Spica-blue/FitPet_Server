from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from openai import OpenAI
import os

from app.db.db import get_session
from app.models.gptDTO import GPTRequest
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
      당신은 맞춤형 식단 및 운동 계획을 제공하는 AI입니다. 사용자가 입력한 정보를 바탕으로 1주일치 식단과 운동량을 구성하여 JSON 형식으로 출력하세요.  
      알레르기 정보에 해당하는 식품은 반드시 제외하고, 그에 맞는 대체 식품을 추천하세요. 예를 들어, "유제품" 알레르기가 있을 경우, 요거트, 치즈, 우유 등을 포함한 모든 유제품을 제외하고, 유제품 대체 식품(예: 아몬드 우유, 코코넛 요거트 등)을 사용해 대체 식단을 제공하세요.

      출력 예시:
      { "식단": { "1일": { "아침": "...(kcal)", "점심": "...(kcal)", "저녁": "...(kcal)" }, ... }, "운동": { "하루 목표 걸음 수": 숫자(예: 10000보) } }

      JSON만 출력하세요. \n, \ 또는 ```json 같은 기호를 포함하지 마세요.
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
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
      ],
      temperature=0.7
    )

    result = response.choices[0].message.content
    print(f"📦 GPT 응답: {result}")

    # DB 저장
    gpt_service = GPTService(db=session)
    status = await gpt_service.create_or_update_recommendation(data.email, result)

    return {"message": f"추천 결과 {status} 완료", "recommendation": result}

  except Exception as e:
    print("🔥 GPT 추천 실패:", str(e))
    raise HTTPException(status_code=500, detail="GPT 추천 생성 실패")
