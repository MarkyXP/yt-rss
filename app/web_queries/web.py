import httpx

async def get_client():
    async with httpx.AsyncClient() as client:
        yield client