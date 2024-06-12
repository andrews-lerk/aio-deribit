from typing import Any

from aio_deribit.api.http.client import HTTPDeribitJRPCClient
from aio_deribit.api.http.urls import HttpURL
from aio_deribit.tools import Mapper

QueryParams = dict[str, Any]


class Trading:
    def __init__(self, client: HTTPDeribitJRPCClient, urls: HttpURL, mapper: Mapper) -> None:
        """
        Class provides Trading API.

        https://docs.deribit.com/#trading

        :param client: HTTP JRPC Client.
        :param urls: HTTP URLs.
        :param mapper: Mapper for responses parsing.
        :return None:
        """
        self._client = client
        self._urls = urls
        self._mapper = mapper
