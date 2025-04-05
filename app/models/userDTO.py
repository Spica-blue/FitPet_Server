from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class SocialUserRequest(BaseModel):
  # id: str
  login_type: str
  nickname: Optional[str] = None
  email: Optional[str] = None
  profile_image: Optional[str] = None

class UserInfoRequest(BaseModel):
  email: str
  gender: str
  age: int
  height: float
  activity_level: str = Field(..., alias="activityLevel")
  current_weight: float = Field(..., alias="currentWeight")
  target_weight: float = Field(..., alias="targetWeight")
  target_date: Optional[date] = Field(None, alias="targetDate")
  target_calories: int = Field(..., alias="targetCalories")
  diet_intensity: Optional[str] = Field(None, alias="dietIntensity")
  diet_type: Optional[str] = Field(None, alias="dietType")

  class Config:
    allow_population_by_field_name = True 
