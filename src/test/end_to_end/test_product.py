import datetime

from fastapi.testclient import TestClient

from manage_products.main import api
from manage_products.models.product_schemas import Product

client = TestClient(api)


def test_create_product(products_route: str, new_random_product: dict):
    response = client.post(products_route, json=new_random_product)
    product_response = Product(**response.json())
    assert response.status_code == 201
    assert type(product_response) is Product
    assert product_response.price == new_random_product["price"]
    assert product_response.name == new_random_product["name"]
    assert product_response.description == new_random_product["description"]
    assert product_response.views == 0
    assert product_response.is_deleted is False


def test_list_products(products_route: str):
    products = [Product(**p) for p in client.get(products_route).json()]
    assert len(products) > 0
    for p in products:
        assert type(p) is Product


def test_get_product(products_route: str, new_random_product: dict):
    source_product = Product(**client.post(products_route, json=new_random_product).json())
    dest_product = Product(**client.get(f"{products_route}/{source_product.id}").json())

    assert source_product.dict(exclude={"created_date", "views"}) == dest_product.dict(
        exclude={"created_date", "views"}
    )
    assert source_product.views + 1 == dest_product.views
    assert source_product.created_date - dest_product.created_date < datetime.timedelta(seconds=1)


def test_delete_product(products_route: str, new_random_product: dict):
    new_product = Product(**client.post(products_route, json=new_random_product).json())
    deleted_product = Product(**client.delete(f"{products_route}/{new_product.id}").json())

    assert new_product.dict(exclude={"created_date", "views", "is_deleted"}) == deleted_product.dict(
        exclude={"created_date", "views", "is_deleted"}
    )
    assert deleted_product.is_deleted is True


def test_get_invalid_item(products_route: str):
    """Assert the server doesn't 500 on an invalid get request ID"""
    invalid_product_id = -1
    response = client.get(f"{products_route}/{invalid_product_id}")
    assert str(invalid_product_id) in response.json()["detail"]
