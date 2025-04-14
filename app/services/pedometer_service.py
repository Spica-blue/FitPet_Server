from datetime import date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.models.pedometer import PedometerRecord
from app.models.pedometerDTO import PedometerCreate

class PedometerService:
  def __init__(self, db: AsyncSession):
    self.db = db

  async def save_daily_steps(self, data: PedometerCreate):
    today = date.today() # 연월일만

    # result = await self.db.execute(
    #   select(PedometerRecord).where(
    #     PedometerRecord.email == data.email,
    #     PedometerRecord.date == today
    #   )
    # )
    # existing = result.scalar_one_or_none()

    # if existing:
    #   existing.step_count = data.step_count
    
    # else:
    #   record = PedometerRecord(
    #     email=data.email,
    #     step_count=data.step_count,
    #     date=today
    #   )
    #   self.db.add(record)

    # await self.db.commit()

    record = PedometerRecord(
      email=data.email,
      step_count=data.step_count,
      date=today
    )

    self.db.add(record)

    try:
      await self.db.commit()
      return "저장"
    except IntegrityError:
      await self.db.rollback()
      return "이미 저장됨"

