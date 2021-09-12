import datetime
from typing import Dict

from pydantic import BaseModel


class ConversionResponse(BaseModel):
    source: str
    success: bool
    timestamp: datetime.datetime
    quotes: Dict[str, float]
