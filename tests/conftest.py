import multiprocessing as mp
from collections.abc import Generator

import pytest
import uvloop
from pytest_asyncio import is_async_test
from pytest_asyncio.plugin import Coroutine

from tests.mocks.ws_server import run


@pytest.fixture(scope="session", autouse=True)
def _mock_ws_serve() -> Generator[None, None, None]:
    """Start WSMockServer process."""
    mp.set_start_method("forkserver")
    event = mp.Event()
    server_process = mp.Process(target=run, args=(event, 51717))
    server_process.start()
    event.wait(timeout=3)
    yield
    server_process.kill()


@pytest.fixture(scope="session", autouse=True)
def event_loop_policy() -> uvloop.EventLoopPolicy:
    """Set uvloop event loop policy for tests."""
    return uvloop.EventLoopPolicy()


def pytest_collection_modifyitems(items: list[Coroutine]) -> None:
    """Run all tests inside the same event loop."""
    pytest_asyncio_tests = (item for item in items if is_async_test(item))
    session_scope_marker = pytest.mark.asyncio(scope="session")
    for async_test in pytest_asyncio_tests:
        async_test.add_marker(session_scope_marker, append=False)
