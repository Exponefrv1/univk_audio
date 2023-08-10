# Search and download songs from VK easily with univk_audio
An easy-to-use library that allows you to search and download audio from VK, bypassing the restriction on obtaining a token to use the VK audio API.

## Key features

*  Doesn't require a VK Audio API token
*  Login + password auth
*  Searching for songs without specific query rules.
*  Downloading songs
*  Supports async

## Requirements
*  [aiofiles](https://pypi.org/project/aiofiles/)
*  [aiohttp](https://pypi.org/project/aiohttp/)
*  [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
*  [httpx](https://pypi.org/project/httpx/)
*  [lxml](https://pypi.org/project/lxml/)
 
## Installation
```
pip install univk_audio
```

## Getting started

### Get authorization cookies

#### As class object:

```python3
# examples/auth_example.py
import asyncio
from univk_audio import AsyncVKAuth

# Example with class object, needs to close session manually

async def get_auth_cookies_example():
    login: str = "79998887776"
    password: str = "password"

    # user_agent is optional:
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"

    auth = AsyncVKAuth(login = login, password = password, user_agent = user_agent)

    # .get_auth_cookies Returns a string with cookies
    # path is optional, if specified - saves cookies in file

    cookies = await auth.get_auth_cookies(path = "cookies.txt")
    await auth.close()

    print(cookies)

asyncio.run(get_auth_cookies_example())
```

#### Async with:

```python3
# examples/auth_with_example.py
import asyncio
from univk_audio import AsyncVKAuth

# Example with 'async with' construction, that closes session automatically

async def get_auth_cookies_with_example():
    login: str = "79998887776"
    password: str = "password"

    # user_agent is optional:
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"

    async with AsyncVKAuth(login = login, password = password, user_agent = user_agent) as auth:

        # .get_auth_cookies Returns a string with cookies
        # path is optional, if specified - saves cookies in file

        cookies = await auth.get_auth_cookies(path = "cookies.txt") 

        print(cookies)

asyncio.run(get_auth_cookies_with_example())
```

### Search for songs

#### As class object:

```python3
# examples/search_example.py
import asyncio
from univk_audio import AsyncVKMusic

# Example with class object, needs to close session manually

async def search_example():
    cookies: str = "Your cookies from auth. See -> examples/auth_example.py"

    # user_agent is optional:
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"

    music = AsyncVKMusic(cookies = cookies, user_agent = user_agent)

    # .search Returns a Dict[str, str]
    # {"*song-title*": "*download-link*"}

    search_results = await music.search(query = "Imagine Dragons - Bones")
    await music.close()

    for title, download_link in search_results.items():
        print(f"{title}\n{download_link}\n" + "-" * 15)

asyncio.run(search_example())
```

#### Async with:

```python3
# examples/search_with_example.py
import asyncio
from univk_audio import AsyncVKMusic

# Example with 'async with' construction, that closes session automatically

async def search_with_example():
    cookies: str = "Your cookies from auth. See -> auth_example.py"

    # user_agent is optional:
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"

    async with AsyncVKMusic(cookies = cookies, user_agent = user_agent) as music:

        # .search Returns a Dict[str, str]
        # {"*song-title*": "*download-link*"}

        search_results = await music.search(query = "Imagine Dragons - Bones")
        for title, download_link in search_results.items():
            print(f"{title}\n{download_link}\n" + "-" * 15)

asyncio.run(search_with_example())
```

### Search and download songs

#### General example of downloading songs from search results:

```python3
# examples/search_and_download_example.py
import asyncio
from univk_audio import AsyncVKMusic

# General example of downloading songs from search results

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
```
