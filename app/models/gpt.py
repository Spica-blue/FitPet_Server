from sqlmodel import SQLModel, Field
from sqlalchemy import Column, DateTime, func, JSON
from typing import Optional
from datetime import datetime

class GPTRecommendation(SQLModel, table=True):
  __tablename__ = "gpt"

  email: str = Field(primary_key=True, foreign_key="users.email")
  recommendations: dict = Field(sa_column=Column(JSON, nullable=False))
  created_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=False), server_default=func.now()))
  # created_at: datetime = Field(default_factory=datetime.utcnow)

