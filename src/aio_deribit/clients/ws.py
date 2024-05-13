import asyncio
import json
import ssl
from types import TracebackType
from typing import Any, AsyncIterator, Self  # noqa: UP035

import certifi
import websockets
from websockets import WebSocketClientProtocol
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK, InvalidHandshake

from aio_deribit.exceptions import (
    WSConnectionClosedError,
    WSConnectionFailError,
    WSOpenConnectionTimeoutError,
    WSRuntimeError,
)

Message = dict[str, Any]
Headers = dict[str, Any] | None


class WSClient:
    def __init__(
        self,
        recv_timeout: int = 15,
        max_queue: int = 10,
        open_timeout: int | None = 10,
        close_timeout: int | None = None,
    ) -> None:
        """
        Class provides base WS client.

        :param recv_timeout: Max server response time in seconds, default 15 seconds.
        :param max_queue: Parameter sets the maximum length of the queue that holds incoming messages.
        :param open_timeout: Timeout for opening the connection in seconds, default 10 seconds.
        :param close_timeout: Parameter defines a maximum wait time for completing
            the closing handshake and terminating the TCP connection,
            use None to disable limitation.
        :return None:
        """
        self._ssl_context = ssl.create_default_context(cafile=certifi.where())

        self.recv_timeout = recv_timeout
        self._max_queue = max_queue
        self._open_timeout = open_timeout
        self._close_timeout = close_timeout

        # active WebSocket connections storage
        self._ws_conn_pool: set[WebSocketClientProtocol] = set()

    async def ws_connect(self, uri: str, headers: Headers = None) -> "WSConnection":
        """
        Connect to the WebSocket server.

        :param uri: URI for connect to the WebSocket server.
        :param headers: Arbitrary HTTP headers to add to the handshake request.
        :return WebSocketClientProtocol:
        """
        try:
            websocket = await websockets.connect(
                uri=uri,
                extra_headers=headers,
                open_timeout=self._open_timeout,
                max_queue=self._max_queue,
                close_timeout=self._close_timeout,
                ssl=self._ssl_context,
            )
        except TimeoutError as err:
            raise WSOpenConnectionTimeoutError from err
        except (OSError, InvalidHandshake) as err:
            raise WSConnectionFailError from err

        self._ws_conn_pool.add(websocket)
        return WSConnection(self, websocket)

    async def close(self, websocket: WebSocketClientProtocol) -> None:
        """
        Close WebSocket connection.

        :param websocket: WebSocketClientProtocol to closing.
        """
        if websocket in self._ws_conn_pool:
            await websocket.close()
            self._ws_conn_pool.remove(websocket)

    async def close_all(self) -> None:
        """Close all WebSocket connections created by WSClient."""
        await asyncio.gather(*[asyncio.create_task(self.close(ws)) for ws in self._ws_conn_pool])

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.close_all()


class WSConnection:
    def __init__(self, ws_client: WSClient, websocket: WebSocketClientProtocol) -> None:
        """
        Class provides active WS connection.

        :param ws_client: WSClient that created the WebSocket connection.
        :param websocket: WebSocketClientProtocol
        :return None:
        """
        self._ws_client = ws_client
        self._websocket = websocket

    async def send(self, msg: Message) -> None:
        """
        Send a message.

        :param msg: Text for message sending.
        :return None:
        """
        try:
            await self._websocket.send(json.dumps(msg))
        except ConnectionClosedError as err:
            raise WSConnectionClosedError from err

    async def recv(self) -> Any:  # noqa: ANN401
        """
        Receive the next message.

        :return Any: Any data.
        """
        try:
            payload = await self._websocket.recv()
        except ConnectionClosedError as err:
            raise WSConnectionClosedError from err
        except RuntimeError as err:
            raise WSRuntimeError from err
        return payload

    async def __aiter__(self) -> AsyncIterator[Any]:
        """Iterate on incoming messages."""
        try:
            while True:
                yield await self.recv()
        except ConnectionClosedOK:
            return

    @property
    def open(self) -> bool:
        """True when the connection is open, False otherwise."""
        return self._websocket.open

    @property
    def recv_timeout(self) -> int:
        """Return recv timeout setup by the WSClient."""
        return self._ws_client.recv_timeout

    async def close(self) -> None:
        """Close WebSocket connection."""
        await self._ws_client.close(self._websocket)
