from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from sqlmodel import select

from app.models.user import SocialUser
from app.models.userDTO import SocialUserRequest
from app.services.base import BaseService

class UserService(BaseService[SocialUser]):
  def __init__(self, db: AsyncSession):
    super().__init__(SocialUser, db)

  async def get_by_id(self, user_id: str) -> SocialUser | None:
    return await self.get(user_id)
  
  async def get_by_email(self, email: str) -> SocialUser | None:
    result = await self.db.execute(
        select(SocialUser).where(SocialUser.email == email)
    )
    return result.scalars().first()
  
  async def create_user(self, user_data: SocialUserRequest) -> SocialUser:
    user_dict = user_data.dict()
    return await self.create(user_dict)
  
  async def update_last_login(self, user_id: str) -> SocialUser | None:
    user = await self.get(user_id)
    if not user:
        return None

    user.last_login_at = datetime.utcnow()
    await self.db.commit()
    await self.db.refresh(user)
    return user
  
  # async def delete_user(self, user_id: str) -> bool:
  #   user = await self.get(user_id)
  #   if not user:
  #       return False
  #   await self.delete(user)
  #   return True
  
  async def delete(self, user: SocialUser) -> None:
    await self.db.delete(user)
    await self.db.commit()

    
  # async def create_user(self)
  
  # async def create_or_update_user(self, user_data: SocialUserRequest) -> SocialUser:
  #   existing_user = await self.get_by_id(user_data.id)

  #   if existing_user:
  #     # last_login_at은 DB가 onupdate=func.now()로 자동 갱신함
  #     await self.db.commit()
  #     await self.db.refresh(existing_user)
  #     return existing_user
    
  #   new_user = SocialUser(
  #     id=user_data.id,
  #     login_type=user_data.login_type,
  #     nickname=user_data.nickname,
  #     email=user_data.email,
  #     profile_image=user_data.profile_image,
  #     # created_at, last_login_at은 DB가 자동으로 처리
  #   )
  #   self.db.add(new_user)
  #   await self.db.commit()
  #   await self.db.refresh(new_user)
  #   return new_user



  # async def create_user(self, user_data: SocialUserRequest) -> SocialUser:
  #   new_user = SocialUser(
  #     id=user_data.id,
  #     login_type=user_data.login_type,
  #     nickname=user_data.nickname,
  #     email=user_data.email,
  #     profile_image=user_data.profile_image
  #   )
  #   self.db.add(new_user)
  #   await self.db.commit()
  #   await self.db.refresh(new_user)
  #   return new_user

  # async def update(self, user_id: str) -> SocialUser | None:
  #   user = await self.get_by_id(user_id)
  #   if not user:
  #     return None
  #   user.last_login_at = datetime.utcnow()
  #   await self.db.commit()
  #   await self.db.refresh(user)
  #   return user
