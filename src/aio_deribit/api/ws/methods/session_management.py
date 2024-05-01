from aio_deribit.api.responses import Response
from aio_deribit.api.ws.client import WSDeribitJRPCClient
from aio_deribit.api.ws.urls import WebsocketURI
from aio_deribit.tools import Mapper


class SessionManagement:
    def __init__(self, client: WSDeribitJRPCClient, urls: WebsocketURI, mapper: Mapper) -> None:
        """
        Class provides Session management API.

        :param client: WS Client.
        :param urls: WS URIs.
        :param mapper: Mapper for responses parsing.
        :return None:
        """
        self._client = client
        self._urls = urls
        self._mapper = mapper

    async def set_heartbeat(self, interval: int) -> Response[str]:
        """
        https://docs.deribit.com/#public-set_heartbeat

        Signals the Websocket connection to send and request heartbeats.

        :param interval: The heartbeat interval in seconds, but not less than 10.
        :return Response[str]: Result with 'ok' string.
        """
        method = self._urls.set_heartbeat
        params = {"interval": interval}
        payload = await self._client.request(method, params)
        return self._mapper.load(payload, Response[str])
