"""Package provides all HTTP API methods for Deribit."""

from .authentication import Authentication

__all__ = (
    # https://docs.deribit.com/#authentication-2
    "Authentication",
)
