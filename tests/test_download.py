import pytest
from univk_audio import AsyncVKMusic


@pytest.mark.asyncio
async def test_song_download():
    cookies = "Was specified during the tests"
    link = "/download.php?id=681896533_456239034;21_b3168630fa6850037a_dcc1e94305febe80dc&hash=cbef26c59e12e0ec31192ee6eaac6fc670304a87e15a8453e113d0aa86108968"
    async with AsyncVKMusic(cookies = cookies) as music:
        is_downloaded = await music.download(link = link, path = f"test.mp3")
        assert is_downloaded == True