from typing import Type, TypeVar, Generic, Optional, List
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import SQLModel, select

ModelType = TypeVar("ModelType", bound=SQLModel)

class BaseService(Generic[ModelType]):
  def __init__(self, model: Type[ModelType], db: AsyncSession):
    self.model = model
    self.db = db

  async def get(self, id: str) -> Optional[ModelType]:
    result = await self.db.execute(select(self.model).where(self.model.id == id))
    return result.scalars().first()
  
  async def get_all(self) -> List[ModelType]:
    result = await self.db.execute(select(self.model))
    return result.scalars().all()

  async def create(self, obj_in: dict) -> ModelType:
    obj = self.model(**obj_in)
    self.db.add(obj)
    await self.db.commit()
    await self.db.refresh(obj)
    return obj

  async def update(self, obj: ModelType, update_data: dict) -> ModelType:
    for key, value in update_data.items():
      setattr(obj, key, value)
    
    # try:
    #   self.db.add(db_obj)
    #   await self.db.commit()
    #   await self.db.refresh(db_obj)
    #   return True
    # except Exception as e:
    #   print(f"Error in update: {str(e)}")
    #   await self.db.rollback()
    #   return False
    self.db.add(obj)
    await self.db.commit()
    await self.db.refresh(obj)
    return obj
    
  # async def delete(self, id: str) -> bool:
  #   obj = await self.get(id)
    
  #   if not obj:
  #     return False
    
  #   try:
  #     await self.db.delete(obj)
  #     await self.db.commit()
  #     return True
  #   except Exception as e:
  #     print(f"Error in delete: {str(e)}")
  #     await self.db.rollback()
  #     return False

  async def delete(self, obj: ModelType) -> None:
    await self.db.delete(obj)
    await self.db.commit()

