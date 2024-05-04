"""Package provides WS API methods for Deribit."""

from .account_management import AccountManagement
from .authentication import Authentication
from .session_management import SessionManagement
from .supporting import Supporting

__all__ = (
    # Authentication - https://docs.deribit.com/#authentication-2
    "Authentication",
    # Session management -https://docs.deribit.com/#session-management
    "SessionManagement",
    # Supporting - https://docs.deribit.com/#supporting
    "Supporting",
    "AccountManagement",
)
