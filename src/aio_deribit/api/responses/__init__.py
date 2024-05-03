"""Package provides all Response models for Deribit API methods."""

from .base import Response
from .models.authentication import Auth
from .models.session_management import CancelOnDisconnect

__all__ = (
    # Base response - https://docs.deribit.com/#response-messages
    "Response",
    # Authentication - https://docs.deribit.com/#authentication-2
    "Auth",
    # Session management - https://docs.deribit.com/#session-management
    "CancelOnDisconnect",
)
