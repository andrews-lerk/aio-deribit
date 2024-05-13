from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

TData = TypeVar("TData")


@dataclass
class Response(Generic[TData]):
    """
    The Deribit JSON-RPC API always responds with a JSON object with the following fields.

    Exclude error field from this model.

    https://docs.deribit.com/#response-messages
    """

    jsonrpc: str
    id_: str
    testnet: bool

    result: TData

    us_in: int
    us_out: int
    us_diff: int


@dataclass
class SubResponse(Generic[TData]):
    """
    Base subscription response model.

    https://docs.deribit.com/#subscriptions
    """

    jsonrpc: str
    method: str
    params: Params[TData]


@dataclass
class Params(Generic[TData]):
    channel: str
    data: TData

    # optional label only for private channels
    label: str | None = None
