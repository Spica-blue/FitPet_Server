from datetime import date as dt_date, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound
from typing import List

from app.models.pedometer import PedometerRecord
from app.models.pedometerDTO import PedometerCreate

class PedometerService:
  def __init__(self, db: AsyncSession):
    self.db = db

  async def save_daily_steps(self, data: PedometerCreate) -> str:
    # today = dt_date.today() # 연월일만
    # 오늘이 아니라 어제 날짜로 저장
    yesterday = dt_date.today() - timedelta(days=1)

    record = PedometerRecord(
      email=data.email,
      step_count=data.step_count,
      date=yesterday
    )

    self.db.add(record)

    try:
      await self.db.commit()
      return "저장"
    except IntegrityError:
      await self.db.rollback()
      return "이미 저장됨"
    
  async def get_steps_range(self, email: str, start_date: dt_date, end_date: dt_date) -> List[PedometerRecord]:
    """
    주어진 기간 동안(양 끝 포함) email의 PedometerRecord를 모두 조회합니다.
    """
    stmt = (
      select(PedometerRecord)
      .where(PedometerRecord.email == email)
      .where(PedometerRecord.date >= start_date)
      .where(PedometerRecord.date <= end_date)
    )
    result = await self.db.execute(stmt)
    return result.scalars().all()

