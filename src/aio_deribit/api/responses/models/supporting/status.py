from dataclasses import dataclass


@dataclass
class Status:
    locked: bool
    locked_currencies: list[str]
