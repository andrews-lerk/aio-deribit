from typing import Any

from aio_deribit.api.responses import Response
from aio_deribit.api.ws.client import WSDeribitJRPCClient
from aio_deribit.api.ws.urls import WebsocketURI
from aio_deribit.tools import Mapper
from aio_deribit.types import Channel


class SubscriptionManagement:
    MAX_LABEL_CHARACTER_LEN = 16

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

    async def subscribe(
        self,
        channels: list[Channel],
        *,
        private: bool = False,
        label: str | None = None,
        access_token: str | None = None,
    ) -> Response[list[str]]:
        """
        https://docs.deribit.com/#public-subscribe

        https://docs.deribit.com/#private-subscribe

        Subscribe to one or more public or private channels.

        :param channels: A list of channels to subscribe to.
        :param private: Specify private or public method to use.
        :param label: Optional label which will be added to notifications of private channels (max 16 characters).
        :param access_token: Optional access token.
        :return Response[list[str]]: Result with list of subscribed channels.
        """
        method = self._urls.private_sub if private else self._urls.public_sub
        params: dict[str, Any] = {"channels": [channel.channel for channel in channels]}
        if label:
            if len(label) > self.MAX_LABEL_CHARACTER_LEN:
                err = "Characters len of label more than 16"
                raise ValueError(err)
            params.update({"label": label})
        result = await self._client.request(method, params, access_token)
        return self._mapper.load(result, Response[list[str]])

    async def unsubscribe(
        self, channels: list[Channel], *, private: bool = False, access_token: str | None = None
    ) -> Response[list[str]]:
        """
        https://docs.deribit.com/#public-unsubscribe

        https://docs.deribit.com/#private-unsubscribe

        Unsubscribe from one or more public or private channels.

        :param channels: A list of channels to unsubscribe from.
        :param private: Specify private or public method to use.
        :param access_token: Optional access token.
        :return Response[list[str]]: Result with list of unsubscribed channels.
        """
        method = self._urls.private_un_sub if private else self._urls.public_un_sub
        params = {"channels": [channel.channel for channel in channels]}
        result = await self._client.request(method, params, access_token)
        return self._mapper.load(result, Response[list[str]])

    async def unsubscribe_all(self, *, private: bool = False, access_token: str | None = None) -> Response[str]:
        """
        https://docs.deribit.com/#public-unsubscribe_all

        https://docs.deribit.com/#private-unsubscribe_all

        Unsubscribe from all the public or private channels subscribed so far.

        :param private: Specify private or public method to use.
        :param access_token: Optional access token.
        :return Response[list[str]]: Result with list of unsubscribed channels.
        """
        method = self._urls.private_un_sub_all if private else self._urls.public_un_sub_all
        result = await self._client.request(method, {}, access_token)
        return self._mapper.load(result, Response[str])
