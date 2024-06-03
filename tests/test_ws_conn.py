import asyncio
import json

import websockets


async def test_ws_conn() -> None:
    """Test connection stability with WSMockServer."""
    async with asyncio.timeout(5), websockets.connect("ws://127.0.0.1:51717") as websocket:
        for _ in range(3):
            await websocket.send(json.dumps({"method": "ping"}))
            assert await websocket.recv() == "pong"
            await asyncio.sleep(0.5)
