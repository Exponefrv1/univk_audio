import pytest
from univk_audio import AsyncVKMusic


@pytest.mark.asyncio
async def test_search():
    cookies = "id=816380914; first_name=Shantel; photo_50=https%3A%2F%2Fvk.com%2Fimages%2Fcamera_50.png"
    async with AsyncVKMusic(cookies = cookies) as music:
        search_results = await music.search(query = "Imagine Dragons - Bones")
        title, download_link = next(iter(search_results.items()))
        assert title == "Imagine Dragons - Bones"
        assert download_link == "/download.php?id=32350711_456239163;35_43a58a32cf9121093e_09a88cef1c4bb81fb3&hash=f208cd6809ec0a6c42625495b9ae032b8809b70485a3c480ccdd0e629ab42e31"