import asyncio
import json
from pathlib import Path
from multiprocessing import Event

from websockets.server import serve, WebSocketServerProtocol


class WSMockServer:
    def __init__(self, responses_path: Path | str) -> None:
        self.responses_path = responses_path

    async def handle_messages(self, websocket: WebSocketServerProtocol) -> None:
        async for message in websocket:
            print(f"server get message: {message}")
            await websocket.send(json.dumps({"message": "hello"}))


async def main(event: Event, port: int, files: Path | str) -> None:
    mock_server = WSMockServer(files)
    async with serve(mock_server.handle_messages, host="127.0.0.1", port=port) as server:
        # signal to parent process that server is started
        event.set()
        await server.serve_forever()


def run(event: Event, port: int) -> None:
    asyncio.run(main(event, port, Path(__file__).parent.parent / "files"))
