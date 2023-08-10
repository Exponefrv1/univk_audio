from typing import Tuple

__all__: Tuple[str, ...] = (
	# Main class
	"AsyncVKMusic",
	# Auth class
	"AsyncVKAuth",
	# VK Music class exceptions
	"InvalidQuery",
	"InvalidPath",
	"SearchSongError",
	"ParserError",
	"ParseLinkError",
	"DownloaderRequestError",
	"DownloaderWriteError",
	# VK Auth class exceptions
	"OAuthRequestError",
	"VKIDRequestError",
	"ConnectAuthRequestError",
	"SendCodeRequestError",
	"GetCookiesRequestError",
	"AuthObjectNotFound",
	"AuthParsingError",
	"CookieWriterError"
)

try:
	from .async_auth import (
		AsyncVKAuth,
		OAuthRequestError,
		VKIDRequestError,
		ConnectAuthRequestError,
		SendCodeRequestError,
		GetCookiesRequestError,
		AuthObjectNotFound,
		AuthParsingError,
		CookieWriterError
	)
	from .async_client import (
		AsyncVKMusic,
		InvalidQuery,
		InvalidPath,
		SearchSongError,
		ParserError,
		ParseLinkError,
		DownloaderRequestError,
		DownloaderWriteError
	)
except ImportError:

	def exit_init() -> None:
		import sys

		print(
			"VKMusic could not run.\n"
			"Looks like required dependencies were not installed.\n"
			"Please make sure you have installed all required dependencies "
			"from requirements.txt file correctly."
		)
		sys.exit(1)

	exit_init()
