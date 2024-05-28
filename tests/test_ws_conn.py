import asyncio

import websockets


async def test_ws_conn() -> None:
    async with asyncio.timeout(5), websockets.connect('ws://127.0.0.1:51717') as websocket:
        for i in range(3):
            await websocket.send("ping")
            await asyncio.sleep(0.5)
