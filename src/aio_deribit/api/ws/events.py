from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any


class EventBus:
    def __init__(self) -> None:
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

    async def emit(self, msg: Any) -> None:
        """Emit message to all listeners."""
        await asyncio.gather(*[listener.add_result(msg) for listener in self._listeners])

    async def clear(self) -> None:
        """Indicate to all listeners that broadcasting messages."""
        await asyncio.gather(*[listener.close() for listener in self._listeners])


class MessagesQueue:
    def __init__(self) -> None:
        self.__msg_queue: asyncio.Queue = asyncio.Queue()

    async def get_result(self) -> Any:
        """Get result from a queue."""
        return await self.__msg_queue.get()

    async def add_result(self, msg: Any) -> None:
        """Put result to a queue."""
        await self.__msg_queue.put(msg)

    async def close(self) -> None:
        """Indicate about stop broadcasting messages."""
        await self.__msg_queue.put(json.dumps({"aio-deribit": "stop broadcasting"}))
