from sqlalchemy import select

from models.user_model import UserTable
from database import new_session


class UserRepository:
    @classmethod
    async def find_by_username(cls, username: str) -> UserTable | None:
        async with new_session() as session:
            query = select(UserTable).where(UserTable.username == username)
            result = await session.execute(query)
            return result.scalar_one_or_none()
    
    @classmethod
    async def create(cls, username: str, hashed_password: str) -> int:
        async with new_session() as session:
            user = UserTable(username=username, hashed_password=hashed_password)
            session.add(user)
            await session.flush()
            await session.commit()
            return user.id
        
    @classmethod
    async def find_by_id(cls, user_id: int) -> UserTable | None:
        async with new_session() as session:
            query = select(UserTable).where(UserTable.id == user_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()