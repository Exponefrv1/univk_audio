import asyncio
from univk_audio import AsyncVKMusic

# Example with 'async with' construction, that closes session automatically

async def search_with_example():

	user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
	cookies: str = "Your cookies from auth. See -> auth_example.py"

	async with AsyncVKMusic(cookies = cookies, user_agent = user_agent) as music:

			# Returns a Dict[str, str]
			# {"*song-title*": "*download-link*"}
			search_results = await music.search(query = "Imagine Dragons - Bones")

			for title, download_link in search_results.items():
				print(f"{title}\n{download_link}\n" + "-" * 15)


asyncio.run(search_with_example())