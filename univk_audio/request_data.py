from typing import (
    Optional,
    Tuple,
    Dict
)


class VKMusicData:

    def __init__(
        self,
        cookies: str,
        user_agent: Optional[str] = None
    ) -> "VKMusicData":

        if user_agent is None:
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"

        self.base_url: str = "https://luxvk.com"
        self.main_headers: Dict[str, str] = {
            "user-agent": user_agent,
            "cookie": f"{cookies} e6885c05e8_blockTimer=1; u_e6885c05e8=1; e6885c05e8_delayCount=6"
        }
        self.download_headers: Dict[str, str] = {
            "user-agent": user_agent
        }


class VKAuthData:

    def __init__(
        self,
        username: str,
        password: str,
        user_agent: Optional[str] = None
    ) -> "VKAuthData":

        if user_agent is None:
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"

        self.links: Tuple[str, ...] = (
                "http://oauth.vk.com/authorize?client_id=6102407&redirect_uri=http://luxvk.com&response_type=code",
                "https://id.vk.com/auth?app_id=6102407&state=&response_type=code&redirect_uri=http%3A%2F%2Fluxvk.com&redirect_uri_hash=194719be504392f684&code_challenge=&code_challenge_method=&return_auth_hash=9283343fd862473e7e&scope=0&force_hash=",
                "https://login.vk.com/?act=connect_authorize",
                "https://api.vk.com/method/auth.getOauthCode?v=5.207&client_id=6102407",
                "http://luxvk.com/"
            )
        self.auth_part_pattern: str = r'"auth":\s*{\s*"(?:\w+|_\w+)"\s*:\s*"(.*?)",\s*"(?:\w+|_\w+)"\s*:\s*"(.*?)",\s*"(?:\w+|_\w+)"\s*:\s*([0-9]+),\s*"(?:\w+|_\w+)"\s*:\s*([0-9]+),\s*"(?:\w+|_\w+)"\s*:\s*([0-9]+)\s*}'
        self.main_headers: Dict[str, str] = {
            "user-agent": user_agent
        }
        self.connect_auth_data: Dict[str, str] = {
            "username": username,
            "password": password,
            "sid": "",
            "uuid": "",
            "v": "5.207",
            "version": 1,
            "app_id": "6102407",
        }
        self.oauth_code_data: Dict[str, str] = {
            "redirect_uri": "http://luxvk.com",
            "app_id": "6102407",
            "hash": "9283343fd862473e7e",
        }
        self.code: Optional[str] = None

