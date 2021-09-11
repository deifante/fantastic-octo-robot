import datetime
from dataclasses import asdict
from unittest.mock import MagicMock, patch

from manage_products.models.product import Product
from manage_products.services.product import get_product


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
