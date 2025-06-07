from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
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
  allergy: Optional[List[str]] = Field(default_factory=list)

  class Config:
    allow_population_by_field_name = True 

class UserInfoResponse(BaseModel):
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
  allergy: List[str] = Field(default_factory=list)

  # Pydantic v2 설정
  model_config = ConfigDict(
    from_attributes=True,
    populate_by_name=True,  # alias가 아닌 field_name(=snake_case)로도 채울 수 있게
    # by_alias=True는 FastAPI response_model에서 자동으로 처리됩니다.
  )
