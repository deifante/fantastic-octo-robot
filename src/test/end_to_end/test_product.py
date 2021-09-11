import pprint

from fastapi.testclient import TestClient

from manage_products.main import api
from manage_products.models.product_schemas import Product

client = TestClient(api)


def test_create_product(products_route: str, new_random_product: dict):
    response = client.post(products_route, json=new_random_product)
    product_response = Product(**response.json())
    assert response.status_code == 201
    assert type(product_response) is Product
    assert product_response.price == new_random_product['price']
    assert product_response.name == new_random_product['name']
    assert product_response.description == new_random_product['description']
    assert product_response.views == 0
    assert product_response.is_deleted is False


def test_list_products(products_route: str):
    response = client.get(products_route)
    products = [Product(**p) for p in response.json()]

    for p in products:
        assert type(p) is Product
# def test_delete_product(products_route: str, new_random_product:dict):
#     new_product = Product(**client.post(products_route, json=new_random_product).json())
#
#     delete_response = client.delete(products_route + new_product.id)
#
