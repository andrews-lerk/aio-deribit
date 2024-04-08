class URLs:
    def __init__(self, testnet: bool) -> None:

        # base URLs
        self.url = "https://www.deribit.com/api/v2"
        self.testnet_url = "https://test.deribit.com/api/v2"

        self.base_url = self.testnet_url if testnet else self.url

        # Authentication - https://docs.deribit.com/?shell#authentication-2
        self.auth = self.base_url + "/public/auth"
        self.exchange_token = self.base_url + "/public/exchange_token"
        self.fork_token = self.base_url + "/public/fork_token"

        # Supporting - https://docs.deribit.com/?shell#supporting
        self.get_time = self.base_url + "/public/get_time"
        self.hello = self.base_url + "/public/hello"
        self.status = self.base_url + "/public/status"
        self.test = self.base_url + "/public/test"
