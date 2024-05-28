import multiprocessing as mp
import time

import pytest
import pytest_asyncio
import uvloop

from .mocks.ws_server import run


@pytest.fixture(scope='session', autouse=True)
def mock_ws_serve() -> None:
    mp.set_start_method('forkserver')
    event = mp.Event()
    server_process = mp.Process(target=run, args=(event, 51717))
    server_process.start()
    event.wait(timeout=3)
    yield
    server_process.kill()


@pytest.fixture(scope="session", autouse=True)
def event_loop_policy():
    return uvloop.EventLoopPolicy()
