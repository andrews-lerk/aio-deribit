from aio_deribit.api.responses import CancelOnDisconnect, Response
from aio_deribit.api.ws.client import WSDeribitJRPCClient
from aio_deribit.api.ws.urls import WebsocketURI
from aio_deribit.tools import Mapper

OK = str


class SessionManagement:
    MIN_HEARTBEAT_INTERVAL = 10

    def __init__(self, client: WSDeribitJRPCClient, urls: WebsocketURI, mapper: Mapper) -> None:
        """
        Class provides Session management API.

        https://docs.deribit.com/#session-management

        :param client: WS Client.
        :param urls: WS URIs.
        :param mapper: Mapper for responses parsing.
        :return None:
        """
        self._client = client
        self._urls = urls
        self._mapper = mapper

    async def set_heartbeat(self, interval: int) -> Response[OK]:
        """
        https://docs.deribit.com/#public-set_heartbeat

        Signals the Websocket connection to send and request heartbeats.

        :param interval: The heartbeat interval in seconds, but not less than 10.
        :return Response[OK]: Result with OK result.
        """
        if interval < self.MIN_HEARTBEAT_INTERVAL:
            raise ValueError(interval)
        method = self._urls.set_heartbeat
        params = {"interval": interval}
        payload = await self._client.request(method, params)
        return self._mapper.load(payload, Response[OK])

    async def disable_heartbeat(self) -> None:
        """
        https://docs.deribit.com/#public-disable_heartbeat

        Stop sending heartbeat messages.

        :return None:
        """
        method = self._urls.disable_heartbeat
        await self._client.request(method, {})

    async def enable_cancel_on_disconnect(self, scope: str, access_token: str | None = None) -> Response[OK]:
        """
        https://docs.deribit.com/#private-enable_cancel_on_disconnect

        Enable Cancel On Disconnect for the connection.
        After enabling Cancel On Disconnect all orders created by the connection
        will be removed when the connection is closed.

        NOTICE It does not affect orders created by other connections - they will remain active!
        When change is applied for the account,
        then every newly opened connection will start with active Cancel on Disconnect.

        :param scope: Specifies if Cancel On Disconnect change should be applied/checked
            for the current connection or the account (default - connection).
        :param access_token: Optional access token.
        :return Response[OK]: Message with OK result.
        """
        method = self._urls.enable_cancel_on_disconnect
        params = {"scope": scope}
        result = await self._client.request(method, params, access_token)
        return self._mapper.load(result, Response[OK])

    async def disable_cancel_on_disconnect(self, scope: str, access_token: str | None = None) -> Response[OK]:
        """
        https://docs.deribit.com/#private-disable_cancel_on_disconnect

        Disable Cancel On Disconnect for the connection.

        When change is applied for the account,
        then every newly opened connection will start with inactive Cancel on Disconnect.

        :param scope: Specifies if Cancel On Disconnect change should be applied/checked
            for the current connection or the account (default - connection).
        :param access_token: Optional access token.
        :return Response[OK]: Message with OK result.
        """
        method = self._urls.disable_cancel_on_disconnect
        params = {"scope": scope}
        result = await self._client.request(method, params, access_token)
        return self._mapper.load(result, Response[OK])

    async def get_cancel_on_disconnect(
        self, scope: str, access_token: str | None = None
    ) -> Response[CancelOnDisconnect]:
        """
        https://docs.deribit.com/#private-get_cancel_on_disconnect

        Read current Cancel On Disconnect configuration for the account.

        :param scope: Specifies if Cancel On Disconnect change should be applied/checked
            for the current connection or the account (default - connection).
        :param access_token: Optional access token.
        :return Response[CancelOnDisconnect]: CancelOnDisconnect response.
        """
        method = self._urls.get_cancel_on_disconnect
        params = {"scope": scope}
        result = await self._client.request(method, params, access_token)
        return self._mapper.load(result, Response[CancelOnDisconnect])
