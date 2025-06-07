from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from app.db.db import get_session
from app.services.calendar_service import CalendarService
from app.models.calendarDTO import CalendarCreate, CalendarRead

router = APIRouter()

@router.post(
  "/",
  response_model=CalendarRead,
  summary="캘린더 기록 저장 또는 업데이트",
  tags=["calendar"]
)
async def save_calendar(
  payload: CalendarCreate,
  session: AsyncSession = Depends(get_session)
):
  service = CalendarService(session)
  try:
    rec = await service.upsert(payload)
    return CalendarRead(**rec.dict())
  except Exception:
    raise HTTPException(status_code=500, detail="일기 저장 실패")
  
@router.get(
  "/",
  response_model=CalendarRead,
  responses={404: {"description": "기록 없음"}},
  summary="특정 날짜 기록 조회",
  tags=["calendar"]
)
async def get_calendar(
  email: str = Query(...),
  date: date = Query(...),
  session: AsyncSession = Depends(get_session)
):
  service = CalendarService(session)
  rec = await service.get(email, date)

  if not rec:
    raise HTTPException(status_code=404, detail="기록 없음")
  
  return CalendarRead(**rec.dict())

@router.get(
  "/all",
  response_model=List[CalendarRead],
  summary="이메일의 모든 캘린더 기록 조회",
  tags=["calendar"]
)
async def get_all_calendar(
  email: str = Query(..., description="사용자 이메일"),
  session: AsyncSession = Depends(get_session)
):
  service = CalendarService(session)
  records = await service.get_all(email)

  # 비어 있어도 빈 리스트를 반환
  return [CalendarRead(**rec.dict()) for rec in records]

@router.delete(
  "/",
  responses={204: {"descripton": "삭제 성공"}, 404: {"description": "없음"}},
  summary="특정 날짜 기록 삭제",
  tags=["calendar"]
)
async def delete_calendar(
  email: str = Query(...),
  date: date = Query(...),
  session: AsyncSession = Depends(get_session)
):
  service = CalendarService(session)
  ok = await service.delete(email, date)

  if not ok:
    raise HTTPException(status_code=404, detail="기록 없음")
  
  return Response(status_code=204)

