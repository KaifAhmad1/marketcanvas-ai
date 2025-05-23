import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from backend.api.main import app as fastapi_app

@pytest.mark.asyncio
async def test_read_root():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "MarketCanvas AI API",
        "version": "1.0.0",
        "status": "running"
    }

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

@pytest.mark.asyncio
async def test_get_node_types():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/node-types")
    assert response.status_code == 200
    data = response.json()
    assert "text_to_image" in data
    assert data["text_to_image"]["name"] == "Text to Image"
