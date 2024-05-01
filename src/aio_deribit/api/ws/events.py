from __future__ import annotations

import asyncio
import json
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator  # noqa: UP035


class EventBus:
    def __init__(self) -> None:
        """Class provides event bus for websocket incoming messages."""
        self._listeners: set[MessagesQueue] = set()

    @asynccontextmanager
    async def new_listener(self) -> AsyncIterator[MessagesQueue]:
        """Connect to listening for incoming messages."""
        event = MessagesQueue()
        self._listeners.add(event)
        try:
            yield event
        finally:
            self._listeners.remove(event)

    async def emit(self, msg: Any) -> None:  # noqa: ANN401
        """Emit message to all listeners."""
        await asyncio.gather(*[listener.add_result(msg) for listener in self._listeners])

    async def clear(self) -> None:
        """Indicate to all listeners that broadcasting messages."""
        await asyncio.gather(*[listener.close() for listener in self._listeners])


class MessagesQueue:
    def __init__(self) -> None:
        """Class provides queue for websocket incoming messages."""
        self.__msg_queue: asyncio.Queue = asyncio.Queue()

    async def get_result(self) -> Any:  # noqa: ANN401
        """Get result from a queue."""
        return await self.__msg_queue.get()

    async def add_result(self, msg: Any) -> None:  # noqa: ANN401
        """Put result to a queue."""
        await self.__msg_queue.put(msg)

    async def close(self) -> None:
        """Put to queue 'stop broadcasting' message."""
        await self.__msg_queue.put(json.dumps({"aio-deribit": "stop broadcasting"}))
