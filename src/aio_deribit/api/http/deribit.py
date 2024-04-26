from aio_deribit.api.retort import _RETORT
from aio_deribit.clients.http import HTTPClient
from aio_deribit.tools import Mapper
from aio_deribit.types import AuthType
from .methods import Authentication
from .urls import HttpURL


class DeribitHTTP:
    def __init__(
        self,
        client: HTTPClient,
        auth_type: AuthType = AuthType.HMAC,
        testnet: bool = False,
    ) -> None:
        """Class provides Deribit HTTP API.

        :param client: Specify HTTP Client.
        :param auth_type: Specify authentication type, do not specify to use HMAC by default.
        :param testnet: Specify URL for HTTP requests, by default production URL.
        """
        self._urls = HttpURL(testnet)
        self._mapper = Mapper(_RETORT)

        self.authentication = Authentication(client, auth_type, self._urls, self._mapper)
