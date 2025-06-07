from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.pet import Pet as PetModel
from app.models.petDTO import PetCreate, PetUpdate
from app.models.feed_inventory import FeedInventory
from app.services.feedInventory_service import FeedInventoryService
from sqlalchemy.exc import IntegrityError

class PetService:
  def __init__(self, db: AsyncSession):
    self.db = db
    self.feed_svc = FeedInventoryService(db)

  async def get_pet(self, email: str) -> PetModel | None:
    return await self.db.get(PetModel, email)

  # async def get_pet(self, email: str) -> Pet:
  #   stmt = select(Pet).where(Pet.email == email)
  #   res = await self.db.execute(stmt)
  #   return res.scalar_one_or_none()

  # async def create_pet(self, data: PetCreate) -> Pet:
  #   pet = Pet(email=data.email, pet_type=data.pet_type)
  #   inv = FeedInventory(email=data.email)
  #   self.db.add_all([pet, inv])
  #   await self.db.commit()
  #   return pet

  async def create_pet(self, dto: PetCreate) -> PetModel:
    # 1) Pet 모델 추가
    pet = PetModel(**dto.dict())
    self.db.add(pet)

    # 2) FeedInventory도 같은 트랜잭션에서 준비
    await self.feed_svc.create_inventory(dto.email)

    # 3) 한 번에 커밋
    try:
      await self.db.commit()
      # Pet, Inventory 모두 DB에 반영됨
      await self.db.refresh(pet)
      return pet
    except IntegrityError:
      await self.db.rollback()
      raise
  
  # async def update_pet(self, email: str, data: PetUpdate) -> Pet:
  #   pet = await self.get_pet(email)
  #   if not pet:
  #     return None
    
  #   if data.pet_type is not None:
  #     pet.pet_type = data.pet_type

  #   if data.satiety is not None:
  #     pet.satiety = data.satiety
    
  #   await self.db.commit()
  #   return pet

  async def update_pet(self, email: str, dto: PetUpdate) -> PetModel | None:
    pet = await self.get_pet(email)
    if not pet:
        return None

    # 변경된 필드만 적용
    if dto.pet_type is not None:
      pet.pet_type = dto.pet_type
    if dto.satiety is not None:
      pet.satiety = dto.satiety

    await self.db.commit()
    await self.db.refresh(pet)
    return pet