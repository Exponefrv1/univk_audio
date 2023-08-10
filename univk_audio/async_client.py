import asyncio
import aiohttp
import aiofiles
import httpx
import re
from bs4 import BeautifulSoup

from types import TracebackType
from typing import (
	Optional,
	Tuple,
	Dict,
	Type
)

from .request_data import VKMusicData
from .client_exceptions import (
	InvalidQuery,
	InvalidPath,
	SearchSongError,
	ParserError,
	ParseLinkError,
	DownloaderRequestError,
	DownloaderWriteError
)

__all__ = (
	"AsyncVKMusic",
	"InvalidQuery",
	"InvalidPath",
	"SearchSongError",
	"ParserError",
	"ParseLinkError",
	"DownloaderRequestError",
	"DownloaderWriteError"
)

class AsyncVKMusic:

	__slots__ = (
		"_req_data",
		"_httpx_session",
		"_aiohttp_session",
		"_loop"
	)

	def __init__(
		self,
		cookies: str,
		user_agent: str = None
	) -> None:
		req_data = VKMusicData(cookies, user_agent)
		httpx_session = httpx.AsyncClient()
		aiohttp_session = aiohttp.ClientSession()
		loop = asyncio.get_event_loop()

		self._req_data = req_data
		self._httpx_session = httpx_session
		self._aiohttp_session = aiohttp_session
		self._loop = loop


	async def __aenter__(self) -> "AsyncVKMusic":
		return self


	def __parse_search(self, data: str) -> Dict[str, str]:
		try:
			soup = BeautifulSoup(data, 'lxml')
			div = soup.find("div", {"class": "col pl"})
			ul = div.find("ul", {"class": "sm2-playlist-bd list-group"})
			elements = ul.find_all("li",
				{"class": "list-group-item justify-content-between list-group-item-action"})
			search_results = {}
			for el in elements:
				link = el.find("a", {"target": "_blank"})
				search_results.update({el.get_text(): link.get("href")})
			return search_results
		except Exception as err:
			raise ParserError("Failed to parse song data") from err


	async def __get_song_link(self, download_link: str) -> str:
		try:
			download_request = await self._httpx_session.get(
					self._req_data.base_url + download_link,
					headers = self._req_data.download_headers
				)
			song_link = str(download_request.headers.get("Location"))
			additional_request = await self._httpx_session.get(
					song_link,
					headers = self._req_data.download_headers
				)
			regex = r"https:\/\/dl01\.dtmp3\.pw\/cs\d+-\d+v\d+\.vkuseraudio\.net\/s\/v1\/ac\/"
			song_link = re.sub(regex, "https://ts01.flac.pw/dl/", song_link)
			song_link = song_link.replace("/index.m3u8?siren=1", ".mp3")
			return song_link
		except Exception as err:
			raise ParseLinkError("Failed to get song download link") from err


	async def __download_song_request(self, song_link: str) -> Tuple[bytes, int]:
		try:
			async with self._aiohttp_session.get(
				song_link,
				headers = self._req_data.download_headers
			) as song_content:
				content_bytes = await song_content.read()
				content_length = int(song_content.headers['Content-Length'])
				return (content_bytes, content_length)
		except aiohttp.client_exceptions.ClientConnectorError as expected_err:
			raise DownloaderRequestError(
					"Failed to send/process download request. Cannot connect to music source. "
					"Try to change your ip adress and location"
				) from expected_err
		except Exception as err:
			raise DownloaderRequestError("Failed to send/process download request") from err


	async def __search(self, query: str):
		try:
			if len(query) == 0 or len(query) > 25:
				raise InvalidQuery("Invalid query provided")
			params = {"q": query, "p": 1}
			search_request = await self._httpx_session.get(
				self._req_data.base_url,
				headers = self._req_data.main_headers,
				params = params
			)
			search_results = await self._loop.run_in_executor(
				None,
				self.__parse_search,
				search_request.text
			)
			return search_results
		except InvalidQuery as expected_err:
			raise expected_err
		except Exception as err:
			raise SearchSongError(f"Failed to search the '{query}'") from err


	async def __download(self, link: str, path: str) -> bool:
		try:
			if len(path) == 0:
				raise InvalidPath("Invalid path provided")
			song_link = await self.__get_song_link(link)
			length = 0
			while length == 0:
				await asyncio.sleep(3)
				content_data = await self.__download_song_request(song_link)
				content, length = content_data[0], content_data[1]
			async with aiofiles.open(path, mode = "wb") as file:
				await file.write(content)
			return True
		except InvalidPath as expected_err:
			raise expected_err
		except FileNotFoundError as expected_err:
			expected_err.strerror = f"Failed to write song content into the file. No such file or directory: '{path}'"
			raise expected_err
		except Exception as err:
			raise DownloaderWriteError("Failed to write song content into the file") from err


	async def search(self, query: str) -> Dict[str, str]:

		"""
			Returns a dictionary in following format:
			{"song title": "link to pass in the download function"}
		"""

		try:
			search_results = await self.__search(query)
			return search_results
		except Exception as err:
			await self.close()
			raise err


	async def download(self, link: str, path: str) -> bool:

		"""
			Returns "True" if file is downloaded,
			otherwise raises DownloaderWriteError exception.
			Works much better with a VPN (if you're from Russia)
		"""

		try:
			is_saved_successfully = await self.__download(link, path)
			return is_saved_successfully
		except Exception as err:
			await self.close()
			raise err


	async def close(self) -> None:
		await self._httpx_session.aclose()
		await self._aiohttp_session.close()


	async def __aexit__(
			self,
			exc_type: Optional[Type[BaseException]],
			exc_val: Optional[BaseException],
			exc_tb: Optional[TracebackType]
		) -> None:
			await self.close()

