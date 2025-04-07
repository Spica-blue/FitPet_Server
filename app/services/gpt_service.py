from app.models.gpt import GPTRecommendation
from app.services.base import BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from datetime import date
import json

class GPTService(BaseService[GPTRecommendation]):
  def __init__(self, db:AsyncSession):
    super().__init__(GPTRecommendation, db)

  async def create_or_update_recommendation(self, email: str, recommendations: str):
    today = date.today()

    result = await self.db.execute(
      select(GPTRecommendation)
      .where(
        and_(
          GPTRecommendation.email == email,
          func.date(GPTRecommendation.created_at) == today
        )
      )
    )
    existing = result.scalar_one_or_none()

    if existing:
      existing.recommendations = json.loads(recommendations)
      await self.db.commit()
      await self.db.refresh(existing)
      return "updated"
    
    else:
      new_rec = GPTRecommendation(
        email=email,
        recommendations=json.loads(recommendations),
        
      )
      self.db.add(new_rec)
      await self.db.commit()
      await self.db.refresh(new_rec)
      return "created"

