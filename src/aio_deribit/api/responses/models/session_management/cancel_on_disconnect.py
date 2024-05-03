from dataclasses import dataclass


@dataclass
class CancelOnDisconnect:
    enabled: bool
    scope: str
