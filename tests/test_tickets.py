import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_create_ticket():
    
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        
        # Create user first
        user = await ac.post("/users/", json={"name": "Boss"})
        user_id = user.json()["id"]

        response = await ac.post("/tickets/", json={
            "title": "Bug",
            "description": "Fix this",
            "user_id": user_id
        })

    assert response.status_code == 200
    assert response.json()["title"] == "Bug"


@pytest.mark.asyncio
async def test_get_tickets():
    
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/tickets/")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)