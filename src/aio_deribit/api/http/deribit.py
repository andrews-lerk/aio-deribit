from .client import HTTPDeribitJRPCClient
from .urls import URLs
from aio_deribit.api.retort import _RETORT
from aio_deribit.clients.http import HTTPClient
from aio_deribit.types import AuthType
from aio_deribit.tools import Mapper


class DeribitHTTP(HTTPDeribitJRPCClient):
    def __init__(
            self,
            client: HTTPClient = HTTPClient(),
            auth_type: AuthType = AuthType.HMAC,
            testnet: bool = False
    ) -> None:
        super().__init__(client, auth_type)

        self._urls = URLs(testnet)
        self._mapper = Mapper(_RETORT)

    # HTTP API methods here
