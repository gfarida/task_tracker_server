from typing import Optional
from sqlalchemy import select
from database import new_session
from models.task_model import TaskTable
from schemas import STask, STaskAdd


class TaskRepository:
    @classmethod
    async def add_one(cls, data: STaskAdd, user_id: int) -> int:
        async with new_session() as session:
            task = TaskTable(**data.model_dump(), user_id=user_id)
            session.add(task) 
            await session.flush()
            await session.commit()
            return task.id

    @classmethod
    async def find_all(cls, limit: int, offset: int, name: Optional[str], user_id: int) -> list[STask]:
        async with new_session() as session:
            query = select(TaskTable).where(TaskTable.user_id == user_id)

            if name:
                query = query.where(TaskTable.name.ilike(f"%{name}%"))

            query = query.offset(offset).limit(limit)
            result = await session.execute(query)

            task_models = result.scalars().all()
            task_schemas = [STask.model_validate(task_model) for task_model in task_models]
            return task_schemas
    
    @classmethod
    async def delete_one(cls, task_id: int, user_id: int) -> bool:
        async with new_session() as session:
            query = select(TaskTable).where(TaskTable.id == task_id, TaskTable.user_id == user_id)
            result = await session.execute(query)
            task = result.scalar_one_or_none()

            if not task:
                return False
            
            await session.delete(task)
            await session.commit()
            return True