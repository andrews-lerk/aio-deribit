from dataclasses import dataclass


@dataclass
class Status:
    locked: str
    locked_indices: list[str] | None = None
