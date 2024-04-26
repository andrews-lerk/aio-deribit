class URLs:
    def __init__(self) -> None:
        # Authentication - https://docs.deribit.com/?shell#authentication-2
        self.auth = "public/auth"
        self.exchange_token = "public/exchange_token"
        self.fork_token = "public/fork_token"
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

        # Account management - https://docs.deribit.com/?python#account-management
        self.get_positions = "private/get_positions"
