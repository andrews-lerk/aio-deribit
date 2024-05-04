"""Package provides all Response models for Deribit API methods."""

from .base import Response
from .models.authentication import Auth
from .models.session_management import CancelOnDisconnect
from .models.supporting import Hello, Status, Test

__all__ = (
    # Base response - https://docs.deribit.com/#response-messages
    "Response",
    # Authentication - https://docs.deribit.com/#authentication-2
    "Auth",
    # Session management - https://docs.deribit.com/#session-management
    "CancelOnDisconnect",
    # Supporting - https://docs.deribit.com/#supporting
    "Hello",
    "Status",
    "Test",
)
