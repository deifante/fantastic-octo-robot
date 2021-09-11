import datetime
from dataclasses import asdict
from unittest.mock import MagicMock, patch

import pytest

from manage_products.models.product import Product
from manage_products.services.product import get_product, ProductServiceException


@patch("manage_products.services.product.sqlite.read")
def test_get_product(mock_sqlite_read: MagicMock, random_product: Product):
    product_dict = asdict(random_product)
    product_id = 12
    product_dict["id"] = product_id
    mock_sqlite_read.return_value = product_dict
    product = get_product(product_id)

    assert type(product) is Product
    assert product.id == product_id
    assert type(product.name) is str
    assert type(product.price) is float
    assert type(product.description) is str
    assert type(product.views) is int
    assert type(product.is_deleted) is bool
    assert type(product.created_date) is datetime.datetime


@patch("manage_products.services.product.sqlite.read")
def test_get_product_exception(mock_sqlite_read: MagicMock):
    product_id = 12
    mock_sqlite_read.return_value = None

    with pytest.raises(ProductServiceException) as pse:
        get_product(product_id)
        assert str(product_id) in str(pse)
