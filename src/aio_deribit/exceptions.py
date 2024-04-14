from typing import Any


class AioDeribitError(Exception):
    """ Base exception for all aio-deribit errors. """


class DeribitBadResponseError(AioDeribitError):
    def __init__(self, error_payload: Any) -> None:
        self.error_payload = error_payload

    def __str__(self) -> str:
        return ("Deribit bad response. "
                f"Error payload: {self.error_payload}")


class HTTPBadResponseError(AioDeribitError):
    def __init__(self, payload: dict[str, Any], status_code: int, reason: str | None = "unknown") -> None:
        self.payload = payload
        self.status_code = status_code
        self.reason = reason

    def __str__(self) -> str:
        return ("HTTP client bad response. "
                f"Status code: {self.status_code}. "
                f"Reason: {self.reason}.")


class HTTPConnectionFailError(AioDeribitError):
    """ Raised if a connection can not be established. """


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


class WSRecvTimeoutError(AioDeribitError):
    """ Raises when WS recv message is too long. """


class HTTPTimeoutError(AioDeribitError):
    """ Raises when HTTP response waiting is too long. """


class InvalidCredentialsError(AioDeribitError):
    """ Raises when it is no credentials for chosen authentication type. """
