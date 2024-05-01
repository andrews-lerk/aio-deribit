from aio_deribit.api.urls import URLs


class HttpURL(URLs):
    def __init__(self, testnet: bool) -> None:
        """
        Class store all HTTP URLs for Deribit.

        :param testnet: Specify URL to use
        :return Nane:
        """
        super().__init__()

        # base URLs
        self.url = "https://www.deribit.com/api/v2/"
        self.testnet_url = "https://test.deribit.com/api/v2/"

        self.base_url = self.testnet_url if testnet else self.url
