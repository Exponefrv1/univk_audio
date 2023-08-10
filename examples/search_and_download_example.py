import asyncio
from univk_audio import AsyncVKMusic


async def search_and_download_example():
    cookies: str = "Your cookies from auth. See -> auth_example.py"

    # user_agent is optional:
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"

    async with AsyncVKMusic(cookies = cookies, user_agent = user_agent) as music:

            # Returns a Dict[str, str]
            # {"*song-title*": "*download-link*"}

            search_results = await music.search(query = "Imagine Dragons - Bones")

            for title, download_link in search_results.items():
                print("Downloading...\n" + f"{title}\n{download_link}")

                is_downloaded = await music.download(link = download_link, path = f"songs/{title}.mp3")

                if is_downloaded:
                    print(f"File saved as {title}.mp3\n" + "-" * 15)

asyncio.run(search_and_download_example())