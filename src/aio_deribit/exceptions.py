class AioDeribitError(Exception):
    """ Base exception for all aio-deribit errors. """


class HTTPBadResponseError(AioDeribitError):
    def __init__(self, status_code: int, reason: str | None = "unknown") -> None:
        self.status_code = status_code
        self.reason = reason

    def __str__(self) -> str:
        return ("HTTP client bad response. "
                f"Status code: {self.status_code}. "
                f"Reason: {self.reason}.")


class MappingError(AioDeribitError):
    """ Raises when impossible to load or dump json data. """


class WSConnectionClosedError(AioDeribitError):
    """ Raised when trying to interact with a closed connection. """


class WSConnectionFailError(AioDeribitError):
    """ Raises when TCP connection fails or the opening handshake fails. """


class WSRuntimeError(AioDeribitError):
    """ If two coroutines call recv concurrently. """


class WSOpenConnectionTimeoutError(AioDeribitError):
    """ Raises when WS connection opening is too long. """


class HTTPTimeoutError(AioDeribitError):
    """ Raises when HTTP response waiting is too long. """
