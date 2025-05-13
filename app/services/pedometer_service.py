from datetime import date as dt_date, timedelta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound

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
    
  async def get_daily_steps(self, email: str, target_date: dt_date) -> int:
    stmt = select(PedometerRecord).where(
      PedometerRecord.email == email,
      PedometerRecord.date == target_date
    )

    result = await self.db.execute(stmt)
    record = result.scalar_one_or_none()

    if record:
      return record.step_count
    
    else:
      # 기록이 없으면 0으로 간주
      return 0

