from dataclasses import dataclass

from aio_deribit.api.responses.base import Response
from aio_deribit.api.client import _hmac

from adaptix import Retort, name_mapping, NameStyle


@dataclass
class SomeResult:
    cost: int
    time: int


raw_data = {
    "jsonrpc": "2.0",
    "id": 2,
    "testnet": False,
    "result": {
        "cost": 1000,
        "time": 2000,
    },
    "usIn": 1,
    "usOut": 2,
    "usDiff": 3
}


def get_result() -> Response[SomeResult]:
    recipe = [
        name_mapping(
            Response,
            name_style=NameStyle.CAMEL,
        ),
    ]
    retort = Retort(recipe=recipe)
    result = retort.load(raw_data, Response[SomeResult])
    print(result)
    url = "https://test.deribit.com/api/v2/private/buy?amount=40&instrument_name=ETH-PERPETUAL&label=market0000234&type=market"
    print(_hmac(url, client_id="mrvormvpomrovj", client_secret="rmpvoi3nvtnj3rtpvoinjopujovtonijroivnotrinvjtroinjv"))

def main():
    get_result()


if __name__ == '__main__':
    main()
