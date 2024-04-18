import asyncio
import copy
import hashlib
import hmac
import json
from typing import Any, AsyncIterator
from uuid import uuid4

from aio_deribit.clients.ws import WSConnection
from aio_deribit.tools import now_utc
from aio_deribit.types import AuthType
from aio_deribit.exceptions import WSRecvTimeoutError, DeribitBadResponseError

Message = Params = dict[str, Any]


class WSDeribitJRPCClient:
    def __init__(self, websocket: WSConnection, auth_type: AuthType = AuthType.HMAC) -> None:
        """
       :param websocket: Active WS connection
       :param auth_type: Specify authentication type to use, do not specify anything to use HMAC by default
       :return None:
       """
        self._websocket = websocket
        self._auth_type = auth_type

        # base msg template
        self._base_msg = {"jsonrpc": "2.0", "id": -0, "method": "", "params": {}}

    async def _request(
            self,
            method: str,
            params: Params,
            client_id: str | None = None,
            client_secret: str | None = None,
            access_token: str | None = None,
            id_: int | None = None
    ) -> Any:
        """
        Send message and receive data one time with defined timeout.

        :param method: Message for sending.
        :return Any: Any data.
        """
        msg = self._prepare_msg(method, params, client_id, client_secret, access_token, id_)
        print(msg)
        await self._websocket.send(msg)
        try:
            async with asyncio.timeout(self._websocket.recv_timeout):
                payload = json.loads(await self._websocket.recv())
                if payload.get("error"):
                    raise DeribitBadResponseError(error_payload=payload.get("error"))
        except TimeoutError as err:
            raise WSRecvTimeoutError from err
        return payload

    async def _subscribe(self, msg: Message) -> AsyncIterator[Any]:
        """
        Send message and iterating on incoming messages.

        :param msg: Message for sending.
        :return AsyncIterator: For iterating on incoming messages.
        """
        await self._websocket.send(msg)
        async for response in self._websocket:
            yield response

    def _prepare_msg(
            self,
            method: str,
            params: Params,
            client_id: str | None = None,
            client_secret: str | None = None,
            access_token: str | None = None,
            id_: int | None = None
    ) -> Message:
        msg = copy.deepcopy(self._base_msg)
        msg.update({"method": method})
        if id_:
            msg.update({"id": str(id_)})
        else:
            msg.pop("id")
        # In this case AuthType.HMAC = AuthType.BASIC,
        # because Derbit WebSocket supports authentication only via client signature.
        if self._auth_type in (AuthType.HMAC, AuthType.BASIC) and client_id and client_secret:
            creds = _prepare_msg_params_with_signature(client_id, client_secret, **params)
            params.update(creds)
        if self._auth_type == AuthType.BEARER and access_token:
            params.update({'access_token': access_token})
        msg.update({"params": params})
        return msg


def _prepare_msg_params_with_signature(
        client_id: str,
        client_secret: str,
        **kwargs: Any
) -> dict[str, Any]:
    timestamp, nonce = now_utc(), str(uuid4())
    signature = hmac.new(
        bytes(client_secret, "latin-1"),
        msg=bytes('{}\n{}\n{}'.format(timestamp, nonce, kwargs.get("data", "")), "latin-1"),
        digestmod=hashlib.sha256
    ).hexdigest().lower()
    msg = {
        "grant_type": "client_signature",
        "client_id": client_id,
        "timestamp": timestamp,
        "signature": signature,
        "nonce": str(nonce),
        "data": ""
    }
    return msg
