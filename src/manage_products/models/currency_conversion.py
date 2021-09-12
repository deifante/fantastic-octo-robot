import datetime
from dataclasses import dataclass

VALID_CURRENCIES = ("USD", "CAD", "EUR", "GBP")
DEFAULT_CURRENCY = "USD"


@dataclass
class Conversion:
    dest: str
    rate: float
    updated_at: datetime.datetime
    source: str = DEFAULT_CURRENCY
