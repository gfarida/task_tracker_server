from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from models.user_model import UserTable
from repositories.task_repository import TaskRepository
from schemas import SStatus, STask, STaskAdd, STaskId
from services.auth_service import AuthService

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.post("", status_code=status.HTTP_201_CREATED)
async def add_task(
    task: STaskAdd, 
    user: UserTable = Depends(AuthService.get_current_user)
) -> STaskId:
    task_id = await TaskRepository.add_one(task, user_id=user.id)
    return STaskId(ok=True, task_id=task_id)

@router.get("")
async def get_tasks(
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
    name: Optional[str] = Query(None),
    user: UserTable = Depends(AuthService.get_current_user)
) -> list[STask]:
    tasks = await TaskRepository.find_all(limit=limit, offset=offset, name=name, user_id=user.id)
    return tasks

@router.delete("/{task_id}")
async def delete_task(
    task_id: int, 
    user: UserTable = Depends(AuthService.get_current_user)
) -> SStatus:
    success = await TaskRepository.delete_one(task_id, user_id=user.id)
    if not success:
        return JSONResponse(
            status_code=404,
            content={"ok": False, "detail": "Task not found"}
        )

    return SStatus(ok=True)