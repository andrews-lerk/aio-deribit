import asyncio
import copy
import json
from typing import Any
from uuid import uuid4

from aio_deribit.clients.ws import WSConnection
from aio_deribit.exceptions import DeribitBadResponseError, WSConnectionClosedError, WSRecvTimeoutError
from .events import EventBus

Message = dict[str, Any]
Payload = Any


class WSDeribitJRPCClient:
    def __init__(self, websocket: WSConnection) -> None:
        """Class provides WS JRPC Client for Deribit.

        :param websocket: Active WS connection
        :return None:
        """
        self._websocket = websocket
        self._events = EventBus()

        self.__listening_task = self._start_listening()

        # base msg template
        self._base_msg = {"jsonrpc": "2.0", "id": -0, "method": "", "params": {}}

    async def request(
        self,
        method: str,
        params: dict[str, Any],
        access_token: str | None = None,
    ) -> Payload:
        """Send message and receive data one time with defined timeout.

        :param access_token:
        :param params:
        :param method: Message for sending.
        :return Any: Any data.
        """
        id_ = str(uuid4())
        msg = self._prepare_msg(method, params, id_, access_token)
        try:
            async with self._events.new_listener() as listener:
                await self._websocket.send(msg)
                async with asyncio.timeout(self._websocket.recv_timeout):
                    while self._websocket.open:
                        payload = json.loads(await listener.get_result())
                        if payload.get("id") == id_:
                            if payload.get("error"):
                                raise DeribitBadResponseError(error_payload=payload.get("error"))
                            break
                        if payload.get("aio-deribit") == "stop broadcasting":
                            raise WSConnectionClosedError
        except TimeoutError as err:
            raise WSRecvTimeoutError from err
        return payload

    async def start_listening(self) -> None:
        """Start websocket listening task.

        This method create asyncio Task that working on background
        and recv incoming messages.
        """
        if not self.__listening_task.done():
            await asyncio.sleep(0)
            return
        self.__listening_task = self._start_listening()
        await asyncio.sleep(0)

    def stop_listening(self) -> None:
        """Stop websocket listening task."""
        if self.__listening_task.done():
            return
        self.__listening_task.cancel()

    def _start_listening(self) -> asyncio.Task[None]:
        task = asyncio.get_running_loop().create_task(self.__listen(), name="aio-deribit WS listening task")
        return task

    async def __listen(self) -> None:
        try:
            async for msg in self._websocket:
                await self._events.emit(msg)
        except asyncio.CancelledError:
            return
        finally:
            await self._events.clear()
        return

    def _prepare_msg(
        self,
        method: str,
        params: dict[str, Any],
        id_: str,
        access_token: str | None = None,
    ) -> Message:
        msg = copy.deepcopy(self._base_msg)
        msg.update({"method": method, "id": id_})
        if access_token:
            params.update({"access_token": access_token})
        msg.update({"params": params})
        return msg
