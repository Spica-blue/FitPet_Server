from datetime import date
from typing import Optional, Tuple
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.diet import Diet
from app.services.base import BaseService

class DietService(BaseService[Diet]):
  def __init__(self, db: AsyncSession):
    super().__init__(Diet, db)

  async def create_or_update_diet(
      self,
      email: str,
      record_date: date,
      breakfast: Optional[str],
      lunch: Optional[str],
      dinner: Optional[str],
  ) -> Tuple[str, Diet]:
    # 이미 존재하는 레코드 조회
    q = select(Diet).where(
      Diet.email == email,
      Diet.date == record_date
    )

    result = await self.db.execute(q)
    existing: Optional[Diet] = result.scalars().first()

    if existing:
      existing.breakfast = breakfast
      existing.lunch = lunch
      existing.dinner = dinner
      await self.db.commit()
      await self.db.refresh(existing)
      return "updated", existing
    
    # 신규 생성
    new = Diet(
      email=email,
      date=record_date,
      breakfast=breakfast,
      lunch=lunch,
      dinner=dinner
    )
    self.db.add(new)
    await self.db.commit()
    await self.db.refresh(new)
    return "created", new
  
  async def get_diet_by_date(
    self,
    email: str,
    record_date: date
  ) -> Optional[Diet]:
    q = select(Diet).where(
      Diet.email == email,
      Diet.date == record_date
    ) 

    result = await self.db.execute(q)
    return result.scalars().first()
