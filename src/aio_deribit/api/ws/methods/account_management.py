from aio_deribit import WSConnection
from aio_deribit.api.ws.client import WSDeribitJRPCClient
from aio_deribit.api.ws.urls import WebsocketURI
from aio_deribit.tools import Mapper
from aio_deribit.types import AuthType


class AccountManagement(WSDeribitJRPCClient):
    def __init__(self, websocket: WSConnection, urls: WebsocketURI, mapper: Mapper) -> None:
        super().__init__(websocket)

        self._urls = urls
        self._mapper = mapper

    async def get_positions(
            self,
            currency: str,
            access_token: str | None = None
    ) -> None:
        method = self._urls.get_positions
        params = {"currency": currency}
        print(await self._request(method, params, access_token=access_token))
