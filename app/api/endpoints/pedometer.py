from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date as dt_date, timedelta
from typing import List

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
  "/records",
  response_model=List[PedometerRead],
  summary="기간 내 만보기 기록 조회",
  description="email, start, end(YYYY-MM-DD) 파라미터로 해당 기간의 기록(없으면 step_count=0) 리스트를 반환합니다.",
  tags=["pedometer"]
)
async def get_pedometer_records(
  email: str = Query(..., description="사용자 이메일"),
  start: dt_date = Query(..., description="시작일, YYYY-MM-DD"),
  end: dt_date = Query(..., description="종료일, YYYY-MM-DD"),
  session: AsyncSession = Depends(get_session),
):
  service = PedometerService(session)

  # 1) DB 에서 실제 저장된 레코드 가져오기
  records = await service.get_steps_range(email, start, end)
  record_map = {rec.date: rec.step_count for rec in records}

  # 2) 날짜 순으로 반복하며, 없는 날은 0으로 채우기
  days = []
  current = start
  while current <= end:
    steps = record_map.get(current, 0)
    days.append(PedometerRead(email=email, step_count=steps, date=current))
    current += timedelta(days=1)

  return days
