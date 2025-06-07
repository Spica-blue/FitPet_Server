from sqlmodel import SQLModel, Field

class FeedInventory(SQLModel, table=True):
  __tablename__ = "feed_inventory"

  email: str = Field(
    default=None,
    foreign_key="pet.email",
    primary_key=True,
    index=True,
  )
  steak_count: int  = Field(default=0, ge=0)
  bone_count: int   = Field(default=0, ge=0)
  kibble_count: int = Field(default=0, ge=0)
  fish_count: int   = Field(default=0, ge=0)
  catnip_count: int = Field(default=0, ge=0)
  milk_count: int   = Field(default=0, ge=0)
  apple_count: int  = Field(default=0, ge=0)
  candy_count: int  = Field(default=0, ge=0)
  carrot_count: int = Field(default=0, ge=0)