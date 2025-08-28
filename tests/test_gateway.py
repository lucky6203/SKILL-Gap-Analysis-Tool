import pytest, httpx

@pytest.mark.asyncio
async def test_health_gateway():
    async with httpx.AsyncClient() as c:
        r = await c.get("http://localhost:8080/health")
        assert r.status_code in (200, 503)
