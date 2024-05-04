from aio_deribit import __version__
from aio_deribit.api.responses import Hello, Response, Status, Test
from aio_deribit.api.ws.client import WSDeribitJRPCClient
from aio_deribit.api.ws.urls import WebsocketURI
from aio_deribit.tools import Mapper


class Supporting:
    def __init__(self, client: WSDeribitJRPCClient, urls: WebsocketURI, mapper: Mapper) -> None:
        """
        Class provides Supporting API.

        https://docs.deribit.com/#supporting

        :param client: WS client.
        :param urls: WS URIs.
        :param mapper: Mapper for responses parsing.
        """
        self._client = client
        self._urls = urls
        self._mapper = mapper

    async def get_time(self) -> Response[int]:
        """
        https://docs.deribit.com/#public-get_time

        Retrieves the current time (in milliseconds).
        This API endpoint can be used to check the clock skew between your software and Deribit systems.

        :return Response[int]: Result with timestamp (milliseconds since the UNIX epoch).
        """
        method = self._urls.get_time
        payload = await self._client.request(method, {})
        return self._mapper.load(payload, Response[int])

    async def hello(self) -> Response[Hello]:
        """
        https://docs.deribit.com/#public-hello

        Method used to introduce the client software connected to Deribit platform over websocket.
        Provided data may have an impact on the maintained connection and will be collected
        for internal statistical purposes. In response, Deribit will also introduce itself.

        :return Response[Hello]: Hello model.
        """
        method = self._urls.hello
        params = {"client_name": "aio-deribit", "client_version": __version__}
        payload = await self._client.request(method, params)
        return self._mapper.load(payload, Response[Hello])

    async def status(self) -> Response[Status]:
        """
        https://docs.deribit.com/#public-status

        Method used to get information about locked currencies

        :return Response[Status]: Status model.
        """
        method = self._urls.status
        payload = await self._client.request(method, {})
        return self._mapper.load(payload, Response[Status])

    async def test(self, expected_result: str | None = None) -> Response[Test]:
        """
        https://docs.deribit.com/#public-test

        Tests the connection to the API server, and returns its version.
        You can use this to make sure the API is reachable, and matches the expected version.

        :param expected_result: Optional value "exception" will trigger an error response.
            This may be useful for testing wrapper libraries.
        :return Response[Test]: Test model.
        """
        method = self._urls.test
        params = {} if not expected_result else {"expected_result": expected_result}
        payload = await self._client.request(method, params)
        return self._mapper.load(payload, Response[Test])
