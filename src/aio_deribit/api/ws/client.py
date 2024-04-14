import asyncio
import json
from typing import Any, AsyncIterator

from aio_deribit.clients.ws import WSConnection
from aio_deribit.types import AuthType
from aio_deribit.exceptions import WSRecvTimeoutError, DeribitBadResponseError

Message = dict[str, Any]


class WSDeribitJRPCClient:
    def __init__(self, websocket: WSConnection, auth_type: AuthType = AuthType.HMAC) -> None:
        """
       :param websocket: Active WS connection
       :param auth_type: Specify authentication type to use, do not specify anything to use HMAC by default
       :return None:
       """
        self._websocket = websocket
        self._auth_type = auth_type

    async def _request(self, msg: Message, id_: int | None = None) -> Any:
        """
        Send message and receive data one time with defined timeout.

        :param msg: Message for sending.
        :return Any: Any data.
        """
        msg = self._prepare_msg(msg, id_)
        await self._websocket.send(msg)
        try:
            async with asyncio.timeout(self._websocket.recv_timeout):
                payload = json.loads(await self._websocket.recv())
                if payload.get("error"):
                    raise DeribitBadResponseError(error_payload=payload.get("error"))
        except TimeoutError as err:
            raise WSRecvTimeoutError from err
        return payload

    async def _subscribe(self, msg: Message) -> AsyncIterator[Any]:
        """
        Send message and iterating on incoming messages.

        :param msg: Message for sending.
        :return AsyncIterator: For iterating on incoming messages.
        """
        await self._websocket.send(msg)
        async for response in self._websocket:
            yield response

    def _prepare_msg(self, msg: Message, id_: int | None = None) -> Message:
        base_msg = {"jsonrpc": "2.0"}
        if id_:
            base_msg.update({"id": str(id_)})
        base_msg.update(msg)
        return base_msg
