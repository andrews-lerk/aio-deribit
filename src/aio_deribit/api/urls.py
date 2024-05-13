class URLs:
    def __init__(self) -> None:
        """Class store all methods available on Deribit API."""
        # Authentication - https://docs.deribit.com/?shell#authentication-2
        self.auth = "public/auth"
        self.exchange_token = "public/exchange_token"  # noqa: S105
        self.fork_token = "public/fork_token"  # noqa: S105
        self.logout = "private/logout"

        # Session management - https://docs.deribit.com/#session-management
        self.set_heartbeat = "public/set_heartbeat"
        self.disable_heartbeat = "public/disable_heartbeat"
        self.enable_cancel_on_disconnect = "private/enable_cancel_on_disconnect"
        self.disable_cancel_on_disconnect = "private/disable_cancel_on_disconnect"
        self.get_cancel_on_disconnect = "private/get_cancel_on_disconnect"

        # Supporting - https://docs.deribit.com/?shell#supporting
        self.get_time = "public/get_time"
        self.hello = "public/hello"
        self.status = "public/status"
        self.test = "public/test"

        # Subscription management - https://docs.deribit.com/#subscription-management
        self.public_sub = "public/subscribe"
        self.public_un_sub = "public/unsubscribe"
        self.public_un_sub_all = "public/unsubscribe_all"
        self.private_sub = "private/subscribe"
        self.private_un_sub = "private/unsubscribe"
        self.private_un_sub_all = "private/unsubscribe_all"

        # Account management - https://docs.deribit.com/?python#account-management
        self.get_positions = "private/get_positions"
