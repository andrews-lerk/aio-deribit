from queue import SimpleQueue
from typing import Any
from contextlib import asynccontextmanager


class EventBus:
    def __init__(self) -> None:
        self._listeners: set[MessagesQueue] = set()

    @asynccontextmanager
    async def new_listener(self):
        """ Connect to listening for incoming messages. """

        event = MessagesQueue()
        self._listeners.add(event)
        try:
            yield event
        finally:
            self._listeners.remove(event)

    def emit(self, msg: Any) -> None:
        """ Emit message to all listeners. """

        for listener in self._listeners:
            listener.add_result(msg)


class MessagesQueue:
    def __init__(self) -> None:
        self.__msg_queue = SimpleQueue()

    def get_result(self) -> Any:
        """ Get result from a queue. """

        return self.__msg_queue.get(block=True)

    def add_result(self, msg: Any) -> None:
        """ Put result to a queue. """

        self.__msg_queue.put(msg)
