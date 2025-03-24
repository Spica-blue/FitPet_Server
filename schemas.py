from pydantic import BaseModel, EmailStr
from datetime import datetime

class RegisterRequest(BaseModel):
  name: str
  email: EmailStr
  password: str
  

