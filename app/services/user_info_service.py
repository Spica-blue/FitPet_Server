from app.models.user_info import UserInfo
from app.models.userDTO import UserInfoRequest
from app.services.base import BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

class UserInfoService(BaseService[UserInfo]):
  def __init__(self, db: AsyncSession):
    self.db = db

  async def create_or_update_user_info(self, data: UserInfoRequest):
    # 기존 유저 정보 있는지 확인
    result = await self.db.execute(select(UserInfo).where(UserInfo.email == data.email))
    user_info = result.scalar_one_or_none()

    if user_info:
      # 업데이트
      for field, value in data.model_dump().items():
        setattr(user_info, field, value)
      
      await self.db.commit()
      await self.db.refresh(user_info)
      return "updated"
    
    else:
      # 생성
      new_info = UserInfo(**data.model_dump())
      self.db.add(new_info)
      await self.db.commit()
      await self.db.refresh(new_info)
      return "created"
    
  async def get_user_info(self, email: str) -> Optional[UserInfo]:
    """
    email에 해당하는 UserInfo 레코드를 반환합니다.
    없으면 None.
    """
    stmt = select(UserInfo).where(UserInfo.email == email)
    result = await self.db.execute(stmt)
    return result.scalar_one_or_none()

