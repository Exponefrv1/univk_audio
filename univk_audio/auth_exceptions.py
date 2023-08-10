from typing import Tuple

__all__: Tuple[str, ...] = (
	"OAuthRequestError",
	"VKIDRequestError",
	"ConnectAuthRequestError",
	"SendCodeRequestError",
	"GetCookiesRequestError",
	"AuthObjectNotFound",
	"AuthParsingError",
	"CookieWriterError"
)

class OAuthRequestError(Exception):
	"""Handle 'OAuth request failed' error"""


class VKIDRequestError(Exception):
	"""Handle 'VK ID request failed' error"""


class ConnectAuthRequestError(Exception):
	"""Handle 'Connect Auth request failed' error"""


class SendCodeRequestError(Exception):
	"""Handle 'Send Code request failed' error"""


class GetCookiesRequestError(Exception):
	"""Handle 'Get Cookies request failed' error"""


class AuthObjectNotFound(Exception):
	"""Handle 'Auth Object Not Found' error"""


class AuthParsingError(Exception):
	"""Handle Auth Parsing function error"""


class CookieWriterError(Exception):
	"""Handle file writing error"""

