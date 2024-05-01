import hashlib
import hmac
import logging
from typing import Any
from uuid import uuid4

from aio_deribit.api.responses import Auth, Response
from aio_deribit.api.ws.client import WSDeribitJRPCClient
from aio_deribit.api.ws.urls import WebsocketURI
from aio_deribit.exceptions import InvalidCredentialsError, WSConnectionClosedError
from aio_deribit.tools import Mapper, now_utc
from aio_deribit.types import AuthType

logger = logging.getLogger(__name__)
MsgParams = dict[str, Any]


class Authentication:
    def __init__(self, client: WSDeribitJRPCClient, urls: WebsocketURI, mapper: Mapper) -> None:
        """
        Class provides Authentication API.

        https://docs.deribit.com/#authentication-2

        :param client: WS client.
        :param urls: WS URIs.
        :param mapper: Mapper for responses parsing.
        """
        self._client = client
        self._urls = urls
        self._mapper = mapper

    async def auth(
        self,
        auth_type: AuthType,
        *,
        client_id: str | None = None,
        client_secret: str | None = None,
        refresh_token: str | None = None,
        **kwargs: MsgParams,
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
        :param kwargs: Parameters for add to JSON message.
            ``data``
                Contains any user specific value.

            ``state``
                Will be passed back in the response.

            ``scope``
                https://docs.deribit.com/#access-scope for details.
        :return Response[Auth]: Auth model.
        """
        method = self._urls.auth
        if auth_type == AuthType.HMAC and client_id and client_secret:
            params = _prepare_msg_params_with_signature(client_id, client_secret, **kwargs)
        elif auth_type == AuthType.BASIC and client_secret and client_secret:
            params = {
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
                **kwargs,
            }
        elif auth_type == AuthType.BEARER and refresh_token:
            params = {"grant_type": "refresh_token", "refresh_token": refresh_token, **kwargs}
        else:
            raise InvalidCredentialsError
        payload = await self._client.request(method, params)
        return self._mapper.load(payload, Response[Auth])

    async def exchange_token(self, refresh_token: str, subject_id: int) -> Response[Auth]:
        """
        https://docs.deribit.com/?shell#public-exchange_token

        Generates a token for a new subject id. This method can be used to switch between subaccounts.
        :param refresh_token: Refresh token
        :param subject_id: New subject id
        :return  Response[Auth]: Auth model.
        """
        method = self._urls.exchange_token
        params = {"refresh_token": refresh_token, "subject_id": subject_id}
        payload = await self._client.request(method, params)
        return self._mapper.load(payload, Response[Auth])

    async def fork_token(self, refresh_token: str, session_name: str) -> Response[Auth]:
        """
        https://docs.deribit.com/?shell#public-fork_token

        Generates a token for a new named session. This method can be used only with session scoped tokens.
        :param refresh_token: Refresh token.
        :param session_name: New session name.
        :return: Response[Auth]: Auth model.
        """
        method = self._urls.fork_token
        params = {"refresh_token": refresh_token, "session_name": session_name}
        payload = await self._client.request(method, params)
        return self._mapper.load(payload, Response[Auth])

    async def logout(self, *, access_token: str | None = None, **kwargs: MsgParams) -> None:
        """
        https://docs.deribit.com/#private-logout

        Gracefully close websocket connection,
        when COD (Cancel On Disconnect) is enabled orders are not cancelled.
        :param access_token: Optional access token.
        :param kwargs: Parameters for add to JSON message.
            ``invalidate_token``
                If value is true all tokens created in current session are invalidated, default: true
        :return:
        """
        method = self._urls.logout
        params = {**kwargs}
        try:
            await self._client.request(method, params, access_token)
        except WSConnectionClosedError:
            logger.info("Websocket connection closed.")


def _prepare_msg_params_with_signature(
    client_id: str,
    client_secret: str,
    **kwargs: MsgParams,
) -> dict[str, Any]:
    timestamp, nonce = now_utc(), str(uuid4())
    signature = (
        hmac.new(
            bytes(client_secret, "latin-1"),
            msg=bytes("{}\n{}\n{}".format(timestamp, nonce, kwargs.get("data", "")), "latin-1"),
            digestmod=hashlib.sha256,
        )
        .hexdigest()
        .lower()
    )
    return {
        "grant_type": "client_signature",
        "client_id": client_id,
        "timestamp": timestamp,
        "signature": signature,
        "nonce": nonce,
        **kwargs,
    }
