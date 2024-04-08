from .client import DeribitJRPCClient
from .urls import URLs
from .retort import _RETORT
from aio_deribit import Client
from aio_deribit.types import AuthType
from aio_deribit.tools import Mapper


class Deribit(DeribitJRPCClient):
    def __init__(self, client: Client, auth_type: AuthType = AuthType.HMAC, testnet: bool = False) -> None:
        super().__init__(client, auth_type)

        self._urls = URLs(testnet)
        self._mapper = Mapper(_RETORT)

    # HTTP API methods here
