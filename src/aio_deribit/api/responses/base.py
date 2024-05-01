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
