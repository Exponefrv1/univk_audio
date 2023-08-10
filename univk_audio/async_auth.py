import aiofiles
import aiohttp
import re

from types import TracebackType
from typing import Optional, Dict, Type

from .request_data import VKAuthData
from .auth_exceptions import (
    OAuthRequestError,
    VKIDRequestError,
    ConnectAuthRequestError,
    SendCodeRequestError,
    GetCookiesRequestError,
    AuthObjectNotFound,
    AuthParsingError,
    CookieWriterError
)

__all__ = (
    "AsyncVKAuth",
    "OAuthRequestError",
    "VKIDRequestError",
    "ConnectAuthRequestError",
    "SendCodeRequestError",
    "GetCookiesRequestError",
    "AuthObjectNotFound",
    "AuthParsingError",
    "CookieWriterError"
)

class AsyncVKAuth:

    __slots__ = (
        "_captcha_solver",
        "_req_data",
        "_session"
    )

    def __init__(
            self,
            login: str,
            password: str,
            captcha_solver: str = "manually",
            user_agent: Optional[str] = None
        ) -> "AsyncVKAuth":

        req_data = VKAuthData(login, password, user_agent)
        session = aiohttp.ClientSession(cookie_jar = aiohttp.CookieJar())

        self._captcha_solver = captcha_solver
        self._req_data = req_data
        self._session = session


    async def __aenter__(self) -> "AsyncVKAuth":
        return self


    async def __send_oauth_request(self) -> None:
        try:
            async with self._session.get(
                self._req_data.links[0],
                headers = self._req_data.main_headers
            ) as oauth_request:
                cookies = self._session.cookie_jar.filter_cookies("http://oauth.vk.com/")
                cookies = "; ".join([str(x)+"="+str(y) for x, y in cookies.items()])
                self._req_data.main_headers.update({"Cookie": cookies})
        except Exception as err:
            raise OAuthRequestError("Failed to send/process 'OAuth' request") from err


    async def __send_vk_id_auth_request(self) -> None:
        try:
            async with self._session.get(
                self._req_data.links[1],
                headers = self._req_data.main_headers
            ) as vk_id_request:
                if vk_id_request.status == 200:
                    response_content = await vk_id_request.text()
                    await self.__parse_auth_part(response_content)
                else:
                    raise VKIDRequestError(
                            f"VK ID returned an error request status code: {vk_id_request.status}"
                        )
        except VKIDRequestError as expected_err:
            raise expected_err
        except Exception as err:
            raise VKIDRequestError("Failed to send/process 'VK ID' request") from err


    async def __parse_auth_part(self, response_content: str) -> None:
        try:
            matches = re.findall(self._req_data.auth_part_pattern, response_content)
            if matches:
                access_token = matches[0][0]
                cookies = self._session.cookie_jar.filter_cookies("https://id.vk.com/")
                cookies = "; ".join([str(x)+"="+str(y) for x, y in cookies.items()])
                self._req_data.connect_auth_data.update({"auth_token": access_token})
                self._req_data.main_headers["Cookie"] = cookies
                self._req_data.main_headers.update(
                        {
                            "Origin": "https://id.vk.com",
                            "Referer": "https://id.vk.com/"
                        }
                    )
            else:
                raise AuthObjectNotFound("Could not find 'auth' object in response content")
        except AuthObjectNotFound as expected_err:
            raise expected_err
        except Exception as err:
            raise AuthParsingError("Failed to parse auth part from response content") from err


    async def __solve_captcha_request(self, captcha_data, solving) -> Dict[str, str]:
        async with self._session.post(
            self._req_data.links[2],
            headers = self._req_data.main_headers,
            data = self._req_data.connect_auth_data
        ) as connect_auth_request:
            return await connect_auth_request.json()


    async def __send_connect_auth_request(self) -> None:
        try:
            async with self._session.post(
                self._req_data.links[2],
                headers = self._req_data.main_headers,
                data = self._req_data.connect_auth_data
            ) as connect_auth_request:
                if connect_auth_request.status == 200:
                    access_token_data = await connect_auth_request.json()
                    if access_token_data.get("type") == "captcha":
                        if self._captcha_solver == "manually":
                            while access_token_data.get("type") == "captcha":
                                print("Please solve the captcha:\n",
                                    access_token_data.get("captcha_img"))
                                answer = str(input("Solving: "))
                                self._req_data.connect_auth_data.update({
                                    "captcha_key": answer,
                                    "captcha_sid": access_token_data.get("captcha_sid"),
                                    "is_refresh_enabled": access_token_data.get("is_refresh_enabled"),
                                    "captcha_ts": access_token_data.get("captcha_ts"),
                                    "captcha_attempt": access_token_data.get("captcha_attempt")
                                })
                                access_token_data = await self.__solve_captcha_request(access_token_data, answer)
                        else:
                            # TODO
                            pass
                    if access_token_data.get("type") == "error":
                        error_code = access_token_data.get("error_code")
                        raise ConnectAuthRequestError(
                                f"Failed to send/process 'Connect Auth' request. Error code: {error_code}"
                            )
                    if access_token_data.get("type") == "okay":
                        access_token = access_token_data.get("data").get("access_token")
                        cookies = self._session.cookie_jar.filter_cookies("https://login.vk.com/")
                        cookies = "; ".join([str(x)+"="+str(y) for x, y in cookies.items()])
                        self._req_data.oauth_code_data.update({"access_token": access_token})
                        self._req_data.main_headers.update({"Cookie": cookies})
                else:
                    raise ConnectAuthRequestError(
                            f"Connect Auth returned an error request status code: {connect_auth_request.status}"
                        )
        except ConnectAuthRequestError as expected_err:
            raise expected_err
        except Exception as err:
            raise ConnectAuthRequestError("Failed to send/process 'Connect Auth' request") from err


    async def __send_oauth_code_request(self) -> None:
        try:
            async with self._session.post(
                self._req_data.links[3],
                headers = self._req_data.main_headers,
                data = self._req_data.oauth_code_data
            ) as oauth_code_request:
                code_data = await oauth_code_request.json()
                self._req_data.code = code_data.get("response")
        except Exception as err:
            raise SendCodeRequestError("Failed to send/process 'OAuth Code' request") from err


    async def __send_get_cookies_request(self) -> str:
        try:
            async with self._session.get(
                self._req_data.links[4],
                params = {"code": self._req_data.code}
            ) as get_cookies_request:
                cookies = self._session.cookie_jar.filter_cookies("http://luxvk.com/")
                cookies = "; ".join([str(x)+"="+str(y) for x, y in cookies.items()])
                return cookies
        except Exception as err:
            raise GetCookiesRequestError("Failed to send/process 'Get Cookies' request") from err


    async def __write_cookies(self, path: str, cookies: str) -> None:
        try:
            async with aiofiles.open(path, mode = "w") as file:
                await file.write(cookies)
        except Exception as err:
            raise CookieWriterError("Failed to write cookie string into the file") from err


    async def get_auth_cookies(self, path: Optional[str] = None) -> str:

        try:
            await self.__send_oauth_request()
            await self.__send_vk_id_auth_request()
            await self.__send_connect_auth_request()
            await self.__send_oauth_code_request()

            cookie_string = await self.__send_get_cookies_request()
            if path is not None:
                await self.__write_cookies(path, cookie_string)
            await self.close()
            return cookie_string
        except Exception as err:
            await self.close()
            raise err


    async def close(self) -> None:
        await self._session.close()


    async def __aexit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType]
        ) -> None:
        await self.close()

