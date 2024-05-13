from aio_deribit.api.responses import Response
from aio_deribit.api.ws.client import WSDeribitJRPCClient
from aio_deribit.api.ws.urls import WebsocketURI
from aio_deribit.tools import Mapper
from aio_deribit.types import Channel


class SubscriptionManagement:
    def __init__(self, client: WSDeribitJRPCClient, urls: WebsocketURI, mapper: Mapper) -> None:
        """
        Class provides Subscription management API.

        https://docs.deribit.com/#subscription-management

        :param client: WS client.
        :param urls: WS URIs.
        :param mapper: Mapper for responses parsing.
        :return None:
        """
        self._client = client
        self._urls = urls
        self._mapper = mapper

    async def subscribe(self, channels: list[Channel]) -> Response[list[str]]:
        """
        https://docs.deribit.com/#public-subscribe

        Subscribe to one or more channels.

        :param channels: A list of channels to subscribe to.
        :return  Response[list[str]]: Result with list of subscribed channels.
        """
        method = self._urls.public_sub
        params = {"channels": [channel.channel for channel in channels]}
        result = await self._client.request(method, params)
        return self._mapper.load(result, Response[list[str]])
