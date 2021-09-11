import datetime
from dataclasses import dataclass


@dataclass
class Product:
    id: int
    name: str
    price: float
    description: str
    views: int = 0
    is_deleted: bool = False
    created_date: datetime.datetime = datetime.datetime.utcnow()
