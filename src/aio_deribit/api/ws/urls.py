from aio_deribit.api.urls import URLs


class WebsocketURI(URLs):
    def __init__(self, testnet: bool) -> None:
        """
        Class store all WS URIs for Deribit.

        :param testnet: Specify URI to use
        :return Nane:
        """
        super().__init__()

        # Base URI
        self.uri = "wss://www.deribit.com/ws/api/v2"
        self.testnet_uri = "wss://test.deribit.com/ws/api/v2"

        self.base_uri = self.uri if not testnet else self.testnet_uri
