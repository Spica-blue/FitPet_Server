from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date as dt_date

from app.db.db import get_session
from app.services.pedometer_service import PedometerService
from app.models.pedometerDTO import PedometerCreate, PedometerRead

router = APIRouter()

@router.post(
  "/record",
  summary="만보기 기록 저장",
  description="하루가 지나면 자동으로 하루동안의 만보기 기록이 DB에 저장됩니다.",
  tags=["pedometer"]
)
async def save_pedometer_record(
  payload: PedometerCreate,
  session: AsyncSession = Depends(get_session)
):
  try:
    service = PedometerService(session)
    result = await service.save_daily_steps(payload)
    return { "message" : f"걸음 수 {result} 완료", "date": dt_date.today().isoformat()}
  
  except Exception as e:
    print("만보기 기록 실패:", str(e))
    raise HTTPException(status_code=500, detail="만보기 기록 저장 실패")

@router.get(
  "/record",
  summary="특정 날짜 만보기 기록 조회",
  response_model=PedometerRead,
  responses={404: {"description": "해당 날짜 기록 없음"}}
)
async def get_pedometer_record(
  email: str = Query(..., description="사용자 이메일"),
  date: dt_date = Query(..., description="조회할 날짜, YYYY-MM-DD 형식"),
  session: AsyncSession = Depends(get_session)
):
  service = PedometerService(session)
  
  try:
    steps = await service.get_daily_steps(email, date)
    return PedometerRead(email=email, step_count=steps, date=date)
  except Exception as e:
    print("만보기 기록 조회 실패: ", str(e))
    raise HTTPException(status_code=500, detail="만보기 기록 조회 실패")
