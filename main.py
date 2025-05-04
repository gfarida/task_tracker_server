from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_tables, delete_tables
from routers.tasks_router import router as tasks_router
from routers.auth_router import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # await delete_tables()
    await create_tables()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Task Tracker Server"
)

app.include_router(router=tasks_router)
app.include_router(router=auth_router)