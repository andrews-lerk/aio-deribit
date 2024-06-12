from aio_deribit.api.http.client import HTTPDeribitJRPCClient
from aio_deribit.api.retort import _RETORT
from aio_deribit.clients.http import HTTPClient
from aio_deribit.tools import Mapper
from aio_deribit.types import AuthType
from .methods import (
    AccountManagement,
    Authentication,
    BlockTrade,
    ComboBooks,
    MarketData,
    Supporting,
    Trading,
    Wallet,
)
from .urls import HttpURL


class DeribitHTTP:
    def __init__(
        self,
        client: HTTPClient,
        auth_type: AuthType = AuthType.HMAC,
        testnet: bool = False,
    ) -> None:
        """
        Class provides Deribit HTTP API.

        :param client: Specify HTTP Client.
        :param auth_type: Specify authentication type, do not specify to use HMAC by default.
        :param testnet: Specify URL for HTTP requests, by default production URL.
        """
        self._client = HTTPDeribitJRPCClient(client, auth_type)
        self._urls = HttpURL(testnet)
        self._mapper = Mapper(_RETORT)

        self.authentication = Authentication(self._client, self._urls, self._mapper)
        self.supporting = Supporting(self._client, self._urls, self._mapper)
        self.market_data = MarketData(self._client, self._urls, self._mapper)
        self.trading = Trading(self._client, self._urls, self._mapper)
        self.combo_books = ComboBooks(self._client, self._urls, self._mapper)
        self.block_trade = BlockTrade(self._client, self._urls, self._mapper)
        self.wallet = Wallet(self._client, self._urls, self._mapper)
        self.account_management = AccountManagement(self._client, self._urls, self._mapper)
