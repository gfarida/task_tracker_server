import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from database import Model, new_session
from main import app

@pytest.fixture(scope="function")
async def test_app():
    DATABASE_URL = "sqlite+aiosqlite:///:memory:"
    engine = create_async_engine(DATABASE_URL, echo=False)
    session_factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

    async def override_session():
        async with session_factory() as session:
            yield session

    app.dependency_overrides[new_session] = override_session
    return app
