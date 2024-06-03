import asyncio
import json
from multiprocessing import Event
from pathlib import Path

from websockets.server import WebSocketServerProtocol, serve


class WSMockServer:
    def __init__(self, responses_path: Path | str) -> None:
        """Class provides WebSocket server for testing purposes."""
        self.responses_path = responses_path

    async def handle_messages(self, websocket: WebSocketServerProtocol) -> None:
        """WebSocket handle messages."""
        async for message in websocket:
            try:
                request = json.loads(message)
                match request.get("method"):
                    case "ping":
                        await websocket.send("pong")
                    case "subscription":
                        ...
                    case _:
                        await websocket.send(self._messages_handler(request.get("method")))
            except ValueError:
                await websocket.send(json.dumps({"error": "unknown"}))

    def _messages_handler(self, request: str) -> str:
        with (self.responses_path / f"{request}.json").open() as fp:
            return json.dumps(json.load(fp))


async def main(event: Event, port: int, files: Path | str) -> None:
    """Start mock websocket server."""
    mock_server = WSMockServer(files)
    async with serve(mock_server.handle_messages, host="127.0.0.1", port=port) as server:
        # signal to parent process that server is started
        event.set()
        await server.serve_forever()


def run(event: Event, port: int) -> None:
    """Entry point for precess of mock websocket server."""
    asyncio.run(main(event, port, Path(__file__).parent.parent / "files"))
