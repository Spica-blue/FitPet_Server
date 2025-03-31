from pydantic import BaseModel, EmailStr
from typing import Optional

class SocialUserRequest(BaseModel):
  # id: str
  login_type: str
  nickname: Optional[str] = None
  email: Optional[str] = None
  profile_image: Optional[str] = None
