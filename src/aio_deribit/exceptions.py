class AioDeribitError(Exception):
    """ Base exception for all aio-deribit errors. """


class HTTPBadResponseError(AioDeribitError):
    def __init__(self, status_code: int, reason: str) -> None:
        self.status_code = status_code
        self.reason = reason

    def __str__(self) -> str:
        return ("HTTP client bad response. "
                f"Status code: {self.status_code}. "
                f"Reason: {self.reason}.")


class MappingError(AioDeribitError):
    """ Raises when impossible to load or dump json data. """


class HTTPTimeoutError(AioDeribitError):
    """ Raises when response waiting is too long. """
