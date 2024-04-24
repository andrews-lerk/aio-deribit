import asyncio
import copy
import json
from typing import Any, AsyncIterator

from aio_deribit.clients.ws import WSConnection
from aio_deribit.exceptions import WSRecvTimeoutError, DeribitBadResponseError
from .events import EventBus

Message = Params = dict[str, Any]


class WSDeribitJRPCClient:
    def __init__(self, websocket: WSConnection) -> None:
        """
       :param websocket: Active WS connection
       :return None:
       """
        self._websocket = websocket
        self._events = EventBus()

        self.__listening_task = self._start_listening()

        # base msg template
        self._base_msg = {"jsonrpc": "2.0", "id": -0, "method": "", "params": {}}

    async def request(
            self, method: str, params: Params, access_token: str | None = None, id_: int | None = None
    ) -> Any:
        """
        Send message and receive data one time with defined timeout.

        :param id_:
        :param access_token:
        :param params:
        :param method: Message for sending.
        :return Any: Any data.
        """
        msg = self._prepare_msg(method, params, access_token, id_)
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

    def start_listening(self):
        if not self.__listening_task.done():
            return None
        self.__listening_task = self._start_listening()

    def _start_listening(self) -> asyncio.Task:
        task = asyncio.create_task(self.__listen(), name="aio-deribit WS listening task")
        return task

    async def __listen(self) -> None:
        try:
            async for msg in self._websocket:
                self._events.emit(msg)
        except asyncio.CancelledError:
            return None
        return None

    def _prepare_msg(
            self, method: str, params: Params, access_token: str | None = None, id_: int | None = None
    ) -> Message:
        msg = copy.deepcopy(self._base_msg)
        msg.update({"method": method})
        if access_token:
            params.update({'access_token': access_token})
        msg.update({"params": params})
        if id_:
            msg.update({"id": str(id_)})
        else:
            msg.pop("id")
        return msg
