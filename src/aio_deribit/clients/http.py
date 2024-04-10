import ssl
from types import TracebackType
from typing import Any, Type

import certifi
from aiohttp import ClientSession, TCPConnector, ClientTimeout
from aiohttp.typedefs import StrOrURL

from aio_deribit.exceptions import HTTPBadResponseError

Headers = dict[str, Any] | None


class HTTPClient:
    def __init__(
            self,
            session: ClientSession | None = None,
            timeout: int | None = None,
            connection_limit: int = 0,
    ) -> None:
        """
        :param session: Aiohttp client session, use None to create new session
        :param timeout: Total number of seconds for the whole request, use None for disable timeout
        :param connection_limit: Total number simultaneous connections, use 0 for disable limit
        :return: None
        """

        self._ssl_context = ssl.create_default_context(cafile=certifi.where())
        self._connector = TCPConnector(ssl=self._ssl_context, limit=connection_limit)
        self._timeout = ClientTimeout(total=timeout)

        if session is not None:
            self._session = session
        else:
            self._session = self._create_session()

        self._bad_status = 400

    def _get_session(self) -> ClientSession:
        """
        Session manager
        :return ClientSession: Current or new session instance
        """
        if not self._session.closed:
            return self._session
        self._session = self._create_session()
        return self._session

    def _create_session(self) -> ClientSession:
        """
        Session builder
        :return ClientSession: New session instance
        """
        return ClientSession(connector=self._connector, timeout=self._timeout)

    async def get(
            self, url: StrOrURL, headers: Headers = None,
    ) -> Any:
        """
        GET request
        :param url: URL to GET request
        :param headers: Optional headers
        :return Any: JSON payload
        """
        async with self._get_session().get(url, headers=headers) as response:
            payload = await response.json()
            if response.status >= self._bad_status:
                raise HTTPBadResponseError(response.status, response.reason)
        return payload

    async def close(self) -> None:
        """
        Close current session
        :return None:
        """
        if not self._session.closed:
            await self._session.close()
        await self._connector.close()

    async def __aenter__(self) -> "HTTPClient":
        return self

    async def __aexit__(
            self,
            exc_type: Type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None,
    ) -> None:
        await self.close()
