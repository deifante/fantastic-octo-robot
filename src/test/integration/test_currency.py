from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from manage_products.main import api
from manage_products.models.product import Product
from manage_products.services.currency import convert_product_currency, CurrencyServiceException

client = TestClient(api)


@patch("manage_products.services.currency.refresh_exchange_rates")
@patch("manage_products.services.currency.sqlite.read")
def test_convert_product_currency(
    mock_sqlite_read: MagicMock, mock_refresh_exchange_rates: MagicMock, random_product: Product
):
    rate = 3
    mock_sqlite_read.return_value = [{"dest": "CAD", "rate": rate, "updated_at": datetime.now().timestamp()}]
    converted_product = convert_product_currency(random_product, "CAD")
    assert random_product.price * rate == converted_product.price


@patch("manage_products.services.currency.refresh_exchange_rates")
@patch("manage_products.services.currency.sqlite.read")
def test_exception_on_invalid_currency(
    mock_sqlite_read: MagicMock, mock_refresh_exchange_rates: MagicMock, random_product: Product
):
    mock_sqlite_read.return_value = None
    invalid_currency_name = "InvalidCurrencyName"
    with pytest.raises(CurrencyServiceException) as cse:
        convert_product_currency(random_product, invalid_currency_name)
        assert str(invalid_currency_name) in str(cse)
