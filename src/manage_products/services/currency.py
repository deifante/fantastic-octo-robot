"""Currency Service """
import datetime
from typing import Dict, Union

import requests

import os
from dotenv import load_dotenv, find_dotenv

from manage_products.db import sqlite
from manage_products.models.currency_conversion import Conversion, VALID_CURRENCIES, DEFAULT_CURRENCY
from manage_products.models.currency_conversion_schemas import ConversionResponse
from manage_products.models.product import Product

load_dotenv(find_dotenv())

API_KEY = os.environ.get("API_KEY")
BASE_URL = "http://apilayer.net/api/live"


class CurrencyServiceException(Exception):
    pass


def refresh_exchange_rates():
    try:
        conversion = get_conversion("CAD")
    except CurrencyServiceException:
        store_conversions(fetch_conversions())
    else:
        if (datetime.datetime.now() - conversion.updated_at) > datetime.timedelta(days=1):
            store_conversions(fetch_conversions())


def convert_product_currency(product: Product, to_currency: str) -> Product:
    refresh_exchange_rates()
    product.price = convert_currency(product.price, to_currency=to_currency)
    return product


def convert_currency(amount: float, to_currency: str) -> float:
    conversion = get_conversion(to_currency)
    return amount * conversion.rate


def fetch_conversions() -> ConversionResponse:
    currency_list = filter(lambda c: c != DEFAULT_CURRENCY, VALID_CURRENCIES)
    currency_string = ",".join(currency_list)
    params = {
        "access_key": API_KEY,
        "currencies": currency_string,
        "source": DEFAULT_CURRENCY,
        "format": 1,
    }
    response = requests.get(f"{BASE_URL}", params=params)
    return ConversionResponse(**response.json())


def store_conversions(conversion_response: ConversionResponse):
    for quote in conversion_response.quotes.items():
        conversion = Conversion(
            source=conversion_response.source,
            dest=quote[0][-3:],
            rate=quote[1],
            updated_at=conversion_response.timestamp,
        )
        store_conversion(conversion)


def store_conversion(conversion: Conversion):
    query = """
    INSERT INTO conversions (dest, rate, updated_at)
    VALUES (?, ?, ?)
    ON CONFLICT (dest)
    DO UPDATE SET rate=excluded.rate, updated_at=excluded.updated_at
    """
    params = (conversion.dest, conversion.rate, conversion.updated_at.timestamp())
    sqlite.write(query=query, params=params)


def get_conversion(currency: str) -> Conversion:
    query = """
    SELECT dest, rate, updated_at
    from conversions
    WHERE dest = ?
    """
    params = (currency,)
    result = sqlite.read(query=query, params=params)
    if result and len(result) == 1:
        return _convert_to_conversion(result[0])
    else:
        currencies_string = ", ".join(VALID_CURRENCIES)
        raise CurrencyServiceException(
            f"Unable to get currency with code: '{currency}'. Valid currencies: {currencies_string}."
        )


def _convert_to_conversion(item: Dict[str, Union[str, float, int]]) -> Conversion:
    return Conversion(
        dest=item["dest"], rate=item["rate"], updated_at=datetime.datetime.fromtimestamp(item["updated_at"])
    )
