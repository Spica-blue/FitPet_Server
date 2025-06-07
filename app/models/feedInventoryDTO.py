from pydantic import BaseModel, Field
from typing import Optional

class FeedInventoryBase(BaseModel):
  steak_count:   int | None = None
  bone_count:    int | None = None
  kibble_count:  int | None = None
  fish_count:    int | None = None
  catnip_count:  int | None = None
  milk_count:    int | None = None
  apple_count:   int | None = None
  candy_count:   int | None = None
  carrot_count:  int | None = None

class FeedInventoryCreate(FeedInventoryBase):
  email: str

class FeedInventoryRead(FeedInventoryBase):
  email: str

class FeedInventoryUpdate(FeedInventoryBase):
  pass
