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
        self._urls = HttpURL(testnet)
        self._mapper = Mapper(_RETORT)

        self.authentication = Authentication(client, auth_type, self._urls, self._mapper)
