import pytest
from typing import AsyncGenerator
from httpx import AsyncClient
from src.backend.main import app

@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client