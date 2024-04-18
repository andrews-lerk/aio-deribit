from types import TracebackType
from typing import Generator, Any, Type

from aio_deribit.clients.ws import WSConnection, WSClient
from .urls import WebsocketURI
from aio_deribit.tools import Mapper
from aio_deribit.api.retort import _RETORT
from .methods import Authentication, AccountManagement
from aio_deribit.types import AuthType

Headers = dict[str, Any] | None


class DeribitWS:
    def __init__(
            self,
            websocket: WSConnection,
            auth_type: AuthType = AuthType.HMAC,
            testnet: bool = False
    ) -> None:

        self._urls = WebsocketURI(testnet)
        self._mapper = Mapper(_RETORT)

        self.authentication = Authentication(websocket, auth_type, self._urls, self._mapper)
        self.account_management = AccountManagement(websocket, auth_type, self._urls, self._mapper)


class Connect:
    def __init__(
            self,
            client: WSClient,
            auth_type: AuthType = AuthType.HMAC,
            testnet: bool = False,
            headers: Headers = None
    ) -> None:
        """
        :param client: WSClient.
        :param auth_type: Authentication type, do not specify to use HMAC by default.
        :param testnet: Specify connection URI to use.
        :param headers: Optional arbitrary HTTP headers to add to the handshake request.
        """
        self._client = client

        self._auth_type = auth_type
        self._testnet = testnet

        self._headers = headers

        self._uri = WebsocketURI(self._testnet).base_uri

    async def __aenter__(self) -> DeribitWS:
        return await self

    async def __aexit__(
            self,
            exc_type: Type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None
    ) -> None:
        await self.websocket.close()

    def __await__(self) -> Generator[Any, None, DeribitWS]:
        return self.__await_impl__().__await__()

    async def __await_impl__(self) -> DeribitWS:
        websocket = await self._client.ws_connect(self._uri, self._headers)
        self.websocket = websocket
        return DeribitWS(websocket, self._auth_type, self._testnet)

    async def close(self) -> None:
        await self.websocket.close()


DeribitConnect = Connect
