from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.models.calendar import CalendarRecord
from app.models.calendarDTO import CalendarCreate

class CalendarService:
  def __init__(self, db: AsyncSession):
    self.db = db

  async def upsert(self, data: CalendarCreate) -> CalendarRecord:
    stmt = select(CalendarRecord).where(
      CalendarRecord.email == data.email,
      CalendarRecord.date == data.date
    )
    result = await self.db.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing:
      existing.note = data.note
      existing.workout_success = data.workout_success
      existing.created_at = datetime.utcnow()
      rec = existing
    
    else:
      rec = CalendarRecord(**data.dict())
      self.db.add(rec)

    await self.db.commit()
    await self.db.refresh(rec)
    
    return rec
  
  async def get(self, email: str, date) -> CalendarRecord | None:
    stmt = select(CalendarRecord).where(
      CalendarRecord.email == email,
      CalendarRecord.date == date
    )

    result = await self.db.execute(stmt)
    return result.scalar_one_or_none()
  
  async def delete(self, email: str, date) -> bool:
    stmt = select(CalendarRecord).where(
      CalendarRecord.email == email,
      CalendarRecord.date == date
    )

    result = await self.db.execute(stmt)
    rec = result.scalar_one_or_none()

    if not rec:
      return False
    
    await self.db.delete(rec)
    await self.db.commit()

    return True
