import pytest
import httpx
from main import app
from tests.conftest import test_app

@pytest.mark.asyncio
async def test_full_flow(test_app):
    transport = httpx.ASGITransport(app=test_app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post("/auth/register", 
                              json={
                                        "username": "testuser", 
                                        "password": "testpass"
                                    })
        assert r.status_code == 201 or r.status_code == 400

        r = await client.post("/auth/login", 
                              data={
                                        "username": "testuser", 
                                        "password": "testpass"
                                   })
        assert r.status_code == 200
        token = r.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        r = await client.post("/tasks", 
            json={
                    "name": "Task1", 
                    "description": "desc"
                 }, 
            headers=headers)
        assert r.status_code == 201
        task_id = r.json()["task_id"]

        r = await client.get("/tasks", headers=headers)
        assert r.status_code == 200
        assert any(t["id"] == task_id for t in r.json())

        r = await client.delete(f"/tasks/{task_id}", headers=headers)
        assert r.status_code == 200
