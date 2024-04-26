import hashlib
import hmac
from typing import Any
from uuid import uuid4

from aio_deribit.api.http.client import HTTPDeribitJRPCClient
from aio_deribit.api.http.urls import HttpURL
from aio_deribit.api.responses import Auth, Response
from aio_deribit.clients.http import HTTPClient
from aio_deribit.exceptions import InvalidCredentialsError
from aio_deribit.tools import Mapper, now_utc, query_builder
from aio_deribit.types import AuthType


class Authentication(HTTPDeribitJRPCClient):
    def __init__(self, client: HTTPClient, auth_type: AuthType, urls: HttpURL, mapper: Mapper) -> None:
        super().__init__(client, auth_type)
        self._urls = urls
        self._mapper = mapper

    async def auth(
        self,
        auth_type: AuthType,
        client_id: str | None = None,
        client_secret: str | None = None,
        refresh_token: str | None = None,
        **kwargs: Any,
    ) -> Response[Auth]:
        """https://docs.deribit.com/#public-auth

        Specify auth type parameter by grand type:

            `client_credentials` - AuthType BASIC

            `client_signature` - AuthType HMAC

            `refresh_token` - AuthType BEARER

        :param auth_type: Specify auth type to use by this method.
        :param client_id: Optional client id, use if AuthType BASIC or AuthType HMAC.
        :param client_secret: Optional client secret, use if AuthType BASIC or AuthType HMAC.
        :param refresh_token: Optional refresh token, use if AuthType BEARER.
        :param kwargs: Parameters for add to query string.
            ``data``
                Contains any user specific value.

            ``state``
                Will be passed back in the response.

            ``scope``
                https://docs.deribit.com/#access-scope for details.
        :return Response[Auth]: Auth model.
        """
        url = self._urls.base_url + self._urls.auth
        if auth_type == auth_type.BASIC and client_id and client_secret:
            url = url + f"?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"
            url += query_builder(**kwargs)
            payload = await self._get(url)
            return self._mapper.load(payload, Response[Auth])
        if auth_type == auth_type.HMAC and client_id and client_secret:
            url = _prepare_url_with_signature(url, client_id, client_secret, **kwargs)
            payload = await self._get(url)
            return self._mapper.load(payload, Response[Auth])
        if auth_type == auth_type.BEARER and refresh_token:
            url += f"?grant_type=refresh_token&refresh_token={refresh_token}"
            url += query_builder(**kwargs)
            payload = await self._get(url)
            return self._mapper.load(payload, Response[Auth])
        raise InvalidCredentialsError

    async def exchange_token(self, refresh_token: str, subject_id: int) -> Response[Auth]:
        """https://docs.deribit.com/?shell#public-exchange_token

        Generates a token for a new subject id. This method can be used to switch between subaccounts.
        :param refresh_token: Refresh token
        :param subject_id: New subject id
        :return  Response[Auth]: Auth model.
        """
        payload = await self._get(
            self._urls.base_url + self._urls.exchange_token + f"?refresh_token={refresh_token}&subject_id={subject_id}",
        )
        return self._mapper.load(payload, Response[Auth])

    async def fork_token(self, refresh_token: str, session_name: str) -> Response[Auth]:
        """https://docs.deribit.com/?shell#public-fork_token

        Generates a token for a new named session. This method can be used only with session scoped tokens.
        :param refresh_token: Refresh token.
        :param session_name: New session name.
        :return: Response[Auth]: Auth model.
        """
        payload = await self._get(
            self._urls.base_url + self._urls.fork_token + f"?refresh_token={refresh_token}&session_name={session_name}",
        )
        return self._mapper.load(payload, Response[Auth])


def _prepare_url_with_signature(
    url: str,
    client_id: str,
    client_secret: str,
    **kwargs: Any,
) -> str:
    timestamp, nonce = now_utc(), uuid4()
    signature = (
        hmac.new(
            bytes(client_secret, "latin-1"),
            msg=bytes("{}\n{}\n{}".format(timestamp, nonce, kwargs.get("data", "")), "latin-1"),
            digestmod=hashlib.sha256,
        )
        .hexdigest()
        .lower()
    )
    url = (
        url
        + (
            f"?grant_type=client_signature"
            f"&client_id={client_id}&timestamp={timestamp}&nonce={nonce}&signature={signature}"
        )
        + query_builder(
            **kwargs,
        )
    )
    return url
