import hashlib
import hmac
from typing import Any
from uuid import uuid4

from aio_deribit import WSConnection
from aio_deribit.api.ws.client import WSDeribitJRPCClient
from aio_deribit.api.ws.urls import WebsocketURI
from aio_deribit.exceptions import InvalidCredentialsError
from aio_deribit.tools import Mapper, now_utc
from aio_deribit.types import AuthType
from aio_deribit.api.responses import (Response, Auth)


class Authentication(WSDeribitJRPCClient):
    def __init__(self, websocket: WSConnection, auth_type: AuthType, urls: WebsocketURI, mapper: Mapper) -> None:
        super().__init__(websocket, auth_type)

        self._urls = urls
        self._mapper = mapper

    async def auth(
            self,
            auth_type: AuthType,
            *,
            client_id: str | None = None,
            client_secret: str | None = None,
            refresh_token: str | None = None,
            id_: int | None = None,
            **kwargs: Any
    ) -> Response[Auth]:
        """
        https://docs.deribit.com/#public-auth

        Specify auth type parameter by grand type:

            `client_credentials` - AuthType BASIC

            `client_signature` - AuthType HMAC

            `refresh_token` - AuthType BEARER

        :param auth_type: Specify auth type to use by this method.
        :param client_id: Optional client id, use if AuthType BASIC or AuthType HMAC.
        :param client_secret: Optional client secret, use if AuthType BASIC or AuthType HMAC.
        :param refresh_token: Optional refresh token, use if AuthType BEARER.
        :param id_: An optional identifier of the request.
                    If it is included, then the response will contain the same identifier.
        :param kwargs: Parameters for add to query string.
            ``data``
                Contains any user specific value.

            ``state``
                Will be passed back in the response.

            ``scope``
                https://docs.deribit.com/#access-scope for details.
        :return Response[Auth]: Auth model.
        """
        method = self._urls.auth
        params = {}
        if auth_type == AuthType.HMAC and client_id and client_secret:
            params.update(**kwargs)
            payload = await self._request(method, params, client_id=client_id, client_secret=client_secret, id_=id_)
        elif auth_type == AuthType.BASIC and client_secret and client_secret:
            params.update(
                {"grant_type": "client_credentials", "client_id": client_id, "client_secret": client_secret, **kwargs}
            )
            payload = await self._request(method, params, id_=id_)
        elif auth_type == AuthType.BEARER and refresh_token:
            params = {"grant_type": "refresh_token", "refresh_token": refresh_token, **kwargs}
            payload = await self._request(method, params, id_=id_)
        else:
            raise InvalidCredentialsError
        return self._mapper.load(payload, Response[Auth])

    async def exchange_token(self, refresh_token: str, subject_id: int, id_: int | None = None) -> Response[Auth]:
        """
       https://docs.deribit.com/?shell#public-exchange_token

       Generates a token for a new subject id. This method can be used to switch between subaccounts.
       :param refresh_token: Refresh token
       :param subject_id: New subject id
       :param id_: An optional identifier of the request.
                   If it is included, then the response will contain the same identifier.
       :return  Response[Auth]: Auth model.
       """
        method = self._urls.exchange_token
        params = {"refresh_token": refresh_token, "subject_id": subject_id}
        payload = await self._request(method, params, id_)
        return self._mapper.load(payload, Response[Auth])

    async def fork_token(self, refresh_token: str, session_name: str, id_: int | None = None) -> Response[Auth]:
        """
       https://docs.deribit.com/?shell#public-fork_token

       Generates a token for a new named session. This method can be used only with session scoped tokens.
       :param refresh_token: Refresh token.
       :param session_name: New session name.
       :param id_: An optional identifier of the request.
                   If it is included, then the response will contain the same identifier.
       :return: Response[Auth]: Auth model.
       """
        method = self._urls.fork_token
        params = {"refresh_token": refresh_token, "session_name": session_name}
        payload = await self._request(msg, id_)
        return self._mapper.load(payload, Response[Auth])
