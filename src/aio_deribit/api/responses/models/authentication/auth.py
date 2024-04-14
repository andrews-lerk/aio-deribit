from dataclasses import dataclass


@dataclass
class Auth:
    access_token: str
    expires_in: int
    refresh_token: str
    scope: str
    token_type: str
    sid: str | None = None
    state: str | None = None
