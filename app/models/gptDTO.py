from pydantic import BaseModel, Field
from typing import Any, List, Optional
from datetime import date, datetime

class GPTRequest(BaseModel):
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
  allergy: Optional[List[str]] = Field(default_factory=list)

  class Config:
    populate_by_name = True

class GPTRecommendationResponse(BaseModel):
  email: str
  recommendations: Any # GPT가 생성한 JSON 응답 그대로 저장/전달
  created_at: datetime

