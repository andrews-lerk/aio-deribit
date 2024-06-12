"""Package provides all HTTP API methods for Deribit."""

from .account_management import AccountManagement
from .authentication import Authentication
from .block_trade import BlockTrade
from .combo_books import ComboBooks
from .market_data import MarketData
from .supporting import Supporting
from .trading import Trading
from .wallet import Wallet

__all__ = (
    # https://docs.deribit.com/#authentication-2
    "Authentication",
    # https://docs.deribit.com/#supporting
    "Supporting",
    # https://docs.deribit.com/#market-data
    "MarketData",
    # https://docs.deribit.com/#trading
    "Trading",
    # https://docs.deribit.com/#combo-books
    "ComboBooks",
    # https://docs.deribit.com/#block-trade
    "BlockTrade",
    # https://docs.deribit.com/#wallet
    "Wallet",
    # https://docs.deribit.com/#account-management
    "AccountManagement",
)
