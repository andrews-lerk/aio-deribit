from aio_deribit import WSConnection
from aio_deribit.api.responses import Response
from aio_deribit.api.ws.client import WSDeribitJRPCClient
from aio_deribit.api.ws.urls import WebsocketURI
from aio_deribit.tools import Mapper


class SessionManagement:
    def __init__(self, client: WSDeribitJRPCClient, urls: WebsocketURI, mapper: Mapper) -> None:

        self._client = client
        self._urls = urls
        self._mapper = mapper

    async def set_heartbeat(self, interval: int):
        method = self._urls.set_heartbeat
        params = {"interval": interval}
        payload = await self._client.request(method, params)
        return self._mapper.load(payload, Response[str])
