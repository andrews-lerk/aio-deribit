from typing import Generic, TypeVar, get_args

from aio_deribit.api.responses import SubDeribitPriceIndex

TData = TypeVar("TData")


class Channel(Generic[TData]):
    def __init__(self, channel: str) -> None:
        """
        Class provides specific channel configuration.

        :param channel: Channel name.
        :return None:
        """
        self._channel: str = channel

    @property
    def channel(self) -> str:
        """Channel name."""
        return self._channel

    @property
    def resp_type(self) -> type[TData]:
        """Response model type."""
        origin = getattr(self, "__orig_class__", None)
        if not origin:
            err = "No generic type for channel"
            raise ValueError(err)
        orig_t: type[TData] = get_args(origin)[0]
        return orig_t


class Channels:
    """
    Class provides all available channels for Deribit subscriptions.

    https://docs.deribit.com/#subscriptions
    """

    _user_access_log = "user.access_log"
    _user_mmp_trigger = "user.mmp_trigger.{index_name}"

    # book
    _book_with_group_and_depth = "book.{instrument_name}.{group}.{depth}.{interval}"
    _book_instrument_name = "book.{instrument_name}.{interval}"

    # user changes
    _user_changes_by_instrument_name = "user.changes.{instrument_name}.{interval}"
    _user_changes_by_kind = "user.changes.{kind}.{currency}.{interval}"

    _rfq = "rfq.{currency}"

    # user combo trades
    _user_combo_trades_by_instrument_name = "user.combo_trades.{instrument_name}.{interval}"
    _user_combo_trades_by_kind = "user.combo_trades.{kind}.{currency}.{interval}"

    _announcements = "announcements"

    # user orders
    _user_orders_by_instrument_name_raw = "user.orders.{instrument_name}.raw"
    _user_orders_by_kind_raw = "user.orders.{kind}.{currency}.raw"
    _user_orders_by_instrument_name = "user.orders.{instrument_name}.{interval}"
    _user_orders_by_kind = "user.orders.{kind}.{currency}.{interval}"

    _deribit_price_index = "deribit_price_index.{index_name}"
    _deribit_price_ranking = "deribit_price_ranking.{index_name}"
    _ticker = "ticker.{instrument_name}.{interval}"
    _quote = "quote.{instrument_name}"
    _perpetual = "perpetual.{instrument_name}.{interval}"

    # trades
    _trades_by_instrument_name = "trades.{instrument_name}.{interval}"
    _trades_by_kind = "trades.{kind}.{currency}.{interval}"

    # platform state
    _platform_state_public = "platform_state.public_methods_state"
    _platform_state = "platform_state"

    _markprice = "markprice.options.{index_name}"
    _user_lock = "user.lock"
    _deribit_volatility_index = "deribit_volatility_index.{index_name}"
    _deribit_price_statistics = "deribit_price_statistics.{index_name}"
    _user_portfolio = "user.portfolio.{currency}"

    # user trades
    _user_trades_by_instrument_name = "user.trades.{instrument_name}.{interval}"
    _user_trades_by_kind = "user.trades.{kind}.{currency}.{interval}"

    _instrument_state = "instrument.state.{kind}.{currency}"
    _chart_trades = "chart.trades.{instrument_name}.{resolution}"
    _estimated_expiration_price = "estimated_expiration_price.{index_name}"
    _incremental_ticker = "incremental_ticker.{instrument_name}"

    @classmethod
    def deribit_price_index(cls, index_name: str) -> Channel[SubDeribitPriceIndex]:
        """Configure and return deribit_price_index channel."""
        return Channel[SubDeribitPriceIndex](cls._deribit_price_index.format(index_name=index_name))
