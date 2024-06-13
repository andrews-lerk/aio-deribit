"""Package provides WS API methods for Deribit."""

from .account_management import AccountManagement
from .authentication import Authentication
from .block_trade import BlockTrade
from .combo_books import ComboBooks
from .market_data import MarketData
from .session_management import SessionManagement
from .subscription_management import SubscriptionManagement
from .supporting import Supporting
from .trading import Trading
from .wallet import Wallet

__all__ = (
    # Authentication - https://docs.deribit.com/#authentication-2
    "Authentication",
    # Session management -https://docs.deribit.com/#session-management
    "SessionManagement",
    # Supporting - https://docs.deribit.com/#supporting
    "Supporting",
    # Subscription management - https://docs.deribit.com/#subscription-management
    "SubscriptionManagement",
    # Market data - https://docs.deribit.com/#market-data
    "MarketData",
    # Trading - https://docs.deribit.com/#trading
    "Trading",
    # Combo books - https://docs.deribit.com/#combo-books
    "ComboBooks",
    # Block trade - https://docs.deribit.com/#block-trade
    "BlockTrade",
    # Wallet - https://docs.deribit.com/#wallet
    "Wallet",
    # Account management - https://docs.deribit.com/#account-management
    "AccountManagement",
)
