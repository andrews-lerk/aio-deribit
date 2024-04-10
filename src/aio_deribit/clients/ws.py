import asyncio
import json
from contextlib import asynccontextmanager
import ssl
from typing import Any, AsyncIterator

import certifi
import websockets
from websockets import WebSocketClientProtocol

Message = dict[str, Any]
Headers = dict[str, Any] | None


class WSClient:
    def __init__(
            self,
            recv_timeout: int = 15,
            open_timeout: int | None = 10,
            close_timeout: int | None = None
    ) -> None:
        """
        :param recv_timeout: Max server response time in seconds, default 15 seconds.
        :param open_timeout: Timeout for opening the connection in seconds, default 10 seconds.
        :param close_timeout: Parameter defines a maximum wait time for completing
        the closing handshake and terminating the TCP connection, use None to disable limitation.
        :return None:
        """
        self._ssl_context = ssl.create_default_context(cafile=certifi.where())
        self._recv_timeout = recv_timeout
        self._open_timeout = open_timeout
        self._close_timeout = close_timeout

        # active WebSocket connections storage
        self._ws_conn_pool: set[WebSocketClientProtocol] = set()

    async def request(self, uri: str, msg: Message, headers: Headers = None) -> Any:
        """
        Opens a WebSocket connection one time and returns a message.

        :param uri: URI for connect to the WebSocket server.
        :param msg: Text for message sending.
        :param headers: Arbitrary HTTP headers to add to the handshake request.
        :return: Any data.
        """

        async with self._ws_connect(uri, headers) as websocket:
            await websocket.send(json.dumps(msg))
            async with asyncio.timeout(self._recv_timeout):
                payload = await websocket.recv()
        return payload

    @asynccontextmanager
    async def subscribe(
            self, uri: str, msg: Message, headers: Headers = None
    ) -> AsyncIterator[WebSocketClientProtocol]:
        """
        Send message and returns an active WebSocket connection through which you
        can iterate asynchronously receiving incoming messages.

        :param uri: URI for connect to the WebSocket server.
        :param msg: Text for message sending.
        :param headers: Arbitrary HTTP headers to add to the handshake request.
        :return WebSocketClientProtocol: Support asynchronous iteration to receive incoming messages.
        """

        async with self._ws_connect(uri, headers) as websocket:
            await websocket.send(json.dumps(msg))
            try:
                yield websocket
            finally:
                await self.close(websocket)

    @asynccontextmanager
    async def _ws_connect(self, uri: str, headers: Headers) -> AsyncIterator[WebSocketClientProtocol]:
        """
        Setup and connect to the WebSocket server.

        :param uri: URI for connect to the WebSocket server.
        :param headers: Arbitrary HTTP headers to add to the handshake request.
        :return WebSocketClientProtocol:
        """

        websocket = await websockets.connect(
            uri=uri,
            extra_headers=headers,
            open_timeout=self._open_timeout,
            close_timeout=self._close_timeout,
            ssl=self._ssl_context
        )
        self._ws_conn_pool.add(websocket)
        try:
            yield websocket
        finally:
            await self.close(websocket)

    async def close(self, websocket: WebSocketClientProtocol) -> None:
        """
        Close WebSocket connection.

        :param websocket: WebSocketClientProtocol to closing.
        """
        if websocket in self._ws_conn_pool:
            await websocket.close()
            self._ws_conn_pool.remove(websocket)

    async def close_all(self) -> None:
        """
        Close all WebSocket connections created by WSClient.
        """
        await asyncio.wait(asyncio.create_task(self.close(ws)) for ws in self._ws_conn_pool)
