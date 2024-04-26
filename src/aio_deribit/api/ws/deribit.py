from collections.abc import Generator
from types import TracebackType
from typing import Any

from aio_deribit.api.retort import _RETORT
from aio_deribit.clients.ws import WSClient, WSConnection
from aio_deribit.tools import Mapper
from .client import WSDeribitJRPCClient
from .methods import AccountManagement, Authentication, SessionManagement
from .urls import WebsocketURI

Headers = dict[str, Any] | None


class DeribitWS:
    def __init__(
        self,
        websocket: WSConnection,
        testnet: bool = False,
    ) -> None:
        self._client = WSDeribitJRPCClient(websocket)
        self._urls = WebsocketURI(testnet)
        self._mapper = Mapper(_RETORT)

        # API
        self.authentication = Authentication(self._client, self._urls, self._mapper)
        self.session_management = SessionManagement(self._client, self._urls, self._mapper)
        self.account_management = AccountManagement(self._client, self._urls, self._mapper)


class Connect:
    def __init__(
        self,
        client: WSClient,
        testnet: bool = False,
    ) -> None:
        """:param client: WSClient.
        :param testnet: Specify connection URI to use.
        """
        self._client = client
        self._testnet = testnet

        self._uri = WebsocketURI(self._testnet).base_uri

    async def __aenter__(self) -> DeribitWS:
        return await self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.websocket.close()

    def __await__(self) -> Generator[Any, None, DeribitWS]:
        return self.__await_impl__().__await__()

    async def __await_impl__(self) -> DeribitWS:
        websocket = await self._client.ws_connect(self._uri)
        self.websocket = websocket
        return DeribitWS(websocket, self._testnet)

    async def close(self) -> None:
        await self.websocket.close()


DeribitConnect = Connect
