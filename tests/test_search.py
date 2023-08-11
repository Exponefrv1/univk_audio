import pytest
from univk_audio import AsyncVKMusic


@pytest.mark.asyncio
async def test_search():
    cookies = "id=816380914; first_name=Shantel; " \
    "photo_50=https%3A%2F%2Fvk.com%2Fimages%2Fcamera_50.png"
    async with AsyncVKMusic(cookies=cookies) as music:
        search_results = await music.search(query="Imagine Dragons - Bones")
        title, download_link = next(iter(search_results.items()))
        assert title == "Imagine Dragons - Bones"
        assert "download.php" in download_link
