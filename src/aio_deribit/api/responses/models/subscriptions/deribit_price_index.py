from dataclasses import dataclass


@dataclass
class SubDeribitPriceIndex:
    index_name: str
    price: float
    timestamp: int
