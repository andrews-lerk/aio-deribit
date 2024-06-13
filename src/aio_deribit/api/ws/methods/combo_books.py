from aio_deribit.api.ws.client import WSDeribitJRPCClient
from aio_deribit.api.ws.urls import WebsocketURI
from aio_deribit.tools import Mapper


class ComboBooks:
    def __init__(self, client: WSDeribitJRPCClient, urls: WebsocketURI, mapper: Mapper) -> None:
        """
        Class provides Combo Books API.

        https://docs.deribit.com/#combo-books

        :param client: WS client.
        :param urls: WS URIs.
        :param mapper: Mapper for responses parsing.
        :return None:
        """
        self._client = client
        self._urls = urls
        self._mapper = mapper
