from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import date

from app.db.db import get_session
from app.models.dietDTO import DietRequest, DietResponse
from app.services.diet_service import DietService

router = APIRouter()

@router.post(
  "/",
  response_model=DietResponse,
  summary="식단 기록 생성 또는 업데이트",
)
async def upsert_diet(
  data: DietRequest,
  session: AsyncSession = Depends(get_session)
):
  service = DietService(db=session)
  status, diet = await service.create_or_update_diet(
    data.email,
    data.date,
    data.breakfast,
    data.lunch,
    data.dinner,
  )
  # 단순히 생성/업데이트 된 객체를 반환합니다.
  return diet

@router.get(
  "/",
  response_model=DietResponse,
  summary="특정 날짜 식단 조회",
)
async def read_diet(
  email: str = Query(..., description="조회할 사용자 이메일"),
  date: date = Query(..., description="조회할 날짜 (YYYY-MM-DD)"),
  session: AsyncSession = Depends(get_session),
):
  service = DietService(db=session)
  diet = await service.get_diet_by_date(email, date)
  
  if not diet:
    raise HTTPException(status_code=404, detail="해당 날짜 식단이 없습니다.")
  
  return diet
