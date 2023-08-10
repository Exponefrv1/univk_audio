import pytest
from univk_audio import AsyncVKAuth


@pytest.mark.asyncio
async def test_auth():
    login = "8613402562575"
    password = "cmkkKFGt58aW"
    async with AsyncVKAuth(login = login, password = password) as auth:
        cookies = await auth.get_auth_cookies() 
        assert cookies == "id=816380914; first_name=Shantel; photo_50=https%3A%2F%2Fvk.com%2Fimages%2Fcamera_50.png"