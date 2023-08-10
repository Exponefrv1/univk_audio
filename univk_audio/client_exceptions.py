from typing import Tuple

__all__: Tuple[str, ...] = (
	"InvalidQuery",
	"InvalidPath",
	"SearchSongError",
	"ParserError",
	"ParseLinkError",
	"DownloaderRequestError",
	"DownloaderWriteError"
)

class InvalidQuery(Exception):
	"""Handle 'invalid query' error"""


class InvalidPath(Exception):
	"""Handle 'invalid path' error"""


class SearchSongError(Exception):
	"""Handle searcher error"""


class ParserError(Exception):
	"""Handle parser error"""


class ParseLinkError(Exception):
	"""Handle link parser error"""


class DownloaderRequestError(Exception):
	"""Handle download request error"""


class DownloaderWriteError(Exception):
	"""Handle file writing errors"""

