from enum import StrEnum


class AuthType(StrEnum):
    """
    Deribit provides 3 authentication methods.

    https://docs.deribit.com/#authentication
    """

    BEARER = "BEARER"  # OAuth 2.0 authentication
    BASIC = "BASIC"  # Basic user credentials
    HMAC = "HMAC"  # Deribit signature credentials
