import pytest
from univk_audio import AsyncVKMusic


@pytest.mark.asyncio
async def test_search():
    cookies = "Was specified during the tests"
    async with AsyncVKMusic(cookies = cookies) as music:
        search_results = await music.search(query = "Imagine Dragons - Bones")
        title, download_link = search_results.items()[0]
        assert title == "Imagine Dragons - Bones"
        assert download_link == "/download.php?id=474499180_456664664;35_ff82cb9e8a703b81be_3799e66f858fae28ac&hash=5181565627933264230e85d7342f181e593cfa6e89a1fc30ce4d70234f90d631"