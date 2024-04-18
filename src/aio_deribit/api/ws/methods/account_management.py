from aio_deribit import WSConnection
from aio_deribit.api.ws.client import WSDeribitJRPCClient
from aio_deribit.api.ws.urls import WebsocketURI
from aio_deribit.tools import Mapper
from aio_deribit.types import AuthType


class AccountManagement(WSDeribitJRPCClient):
    def __init__(self, websocket: WSConnection, auth_type: AuthType, urls: WebsocketURI, mapper: Mapper) -> None:
        super().__init__(websocket, auth_type)

        self._urls = urls
        self._mapper = mapper

    async def get_positions(
            self,
            currency: str,
            client_id: str | None = None,
            client_secret: str | None = None,
            access_token: str | None = None
    ) -> None:
        method = self._urls.get_positions
        params = {"currency": currency}
        print(await self._request(method, params, client_id=client_id, client_secret=client_secret, access_token=access_token))
