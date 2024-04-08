import base64
from uuid import uuid4
import hashlib
from urllib.parse import urlparse
import hmac
from typing import Any

from aiohttp.typedefs import StrOrURL

from aio_deribit.base_client import Client
from aio_deribit.types import AuthType
from aio_deribit.exceptions import HTTPTimeoutError
from aio_deribit.tools import now_utc

Headers = dict[str, Any] | None


class DeribitJRPCClient:
    def __init__(self, client: Client, auth_type: AuthType = AuthType.HMAC) -> None:
        """
        :param client: Base HTTP client
        :param auth_type: Specify authentication type to use, do not specify anything to use HMAC by default
        :return None:
        """
        self._client = client
        self._auth_type = auth_type

    async def _get(
            self,
            url: StrOrURL,
            client_id: str | None = None,
            client_secret: str | None = None,
            access_token: str | None = None
    ) -> Any:
        """
        GET request.

        If HMAC (Deribit signature credentials) or BASIC (Basic user credentials) methods are used:
            only client_id and client_secret are used in function

        If BEARER (OAuth 2.0):
            only access_token are used in function

        :param url: URL to GET request
        :param client_id: Optional Client ID if request is private
        :param client_secret: Optional Client Secret if request is private
        :param access_token: Optional Access Token if request is private
        :return Any:
        """

        try:
            payload = await self._client.get(url, self._prepare_headers(url, client_id, client_secret, access_token))
        except TimeoutError as err:
            raise HTTPTimeoutError from err
        return payload

    def _prepare_headers(
            self,
            url: StrOrURL,
            client_id: str | None = None,
            client_secret: str | None = None,
            access_token: str | None = None
    ) -> Headers:
        """
        Define needed auth method and return headers

        :param url: URL to GET request
        :param client_id: Optional Client ID if request is private
        :param client_secret: Optional Client Secret if request is private
        :param access_token: Optional Access Token if request is private
        :return Headers: Optional headers if request is private
        """
        if client_id and client_secret and self._auth_type.HMAC:
            return _hmac(url, client_id, client_secret)
        if client_id and client_secret and self._auth_type.BASIC:
            return {"Authorization": f"Basic {base64.b64encode(client_id.encode()+b":"+client_secret.encode())}"}
        if access_token and self._auth_type.BEARER:
            return {"Authorization": f"bearer {access_token}"}
        return None


def _hmac(
        url: StrOrURL,
        client_id: str,
        client_secret: str,
) -> Headers:
    """
    :param url: URL to GET request
    :param client_id: Optional Client ID if request is private
    :param client_secret: Optional Client Secret if request is private
    :return Headers: Authorization header (deri-hmac-sha256)
    """
    parsed_url = urlparse(url)
    uri = parsed_url.path + "?" + parsed_url.query if parsed_url.query else parsed_url.path
    ts, nonce = now_utc(), uuid4()
    signature = hmac.new(
        bytes(client_secret, "latin-1"),
        msg=bytes('{}\n{}\n{}\n{}\n\n'.format(ts, nonce, "GET", uri), "latin-1"),
        digestmod=hashlib.sha256
    ).hexdigest().lower()
    return {"Authorization": f"deri-hmac-sha256 id={client_id},ts={ts},sig={signature},nonce={nonce}"}
