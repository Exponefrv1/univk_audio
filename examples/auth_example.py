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