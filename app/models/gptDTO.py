from pydantic import BaseModel
from typing import Any

class GPTRecommendationResponse(BaseModel):
  email: str
  recommendations: Any
  created_at: str

