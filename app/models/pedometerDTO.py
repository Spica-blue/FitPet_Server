from pydantic import BaseModel

class PedometerCreate(BaseModel):
  email: str
  step_count: int

