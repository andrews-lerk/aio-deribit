"""Package provides all Response models for Deribit API methods."""

from .base import Response
from .models.authentication import Auth

__all__ = (
    # Base response - https://docs.deribit.com/#response-messages
    "Response",
    # Authentication - https://docs.deribit.com/#authentication-2
    "Auth",
)
