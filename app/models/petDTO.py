from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class PetCreate(BaseModel):
  email: str
  pet_type: str
  satiety: Optional[int] = Field(50, ge=0, le=100)   # 기본값 50

class PetRead(BaseModel):
  email: str
  pet_type: str
  satiety: int
  created_at: datetime

  class Config:
    orm_mode = True

class PetUpdate(BaseModel):
  pet_type: Optional[str] = None
  satiety:  Optional[int] = Field(None, ge=0, le=100)