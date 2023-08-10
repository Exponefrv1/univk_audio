import pytest
from univk_audio import AsyncVKAuth


@pytest.mark.asyncio
async def test_auth():
    login = "Was specified during the tests"
    password = "Was specified during the tests"
    async with AsyncVKAuth(login = login, password = password) as auth:
        cookies = await auth.get_auth_cookies(path = "cookies.txt") 
        assert cookies == "Was specified during the tests"