from fastapi.testclient import TestClient

from manage_products.main import api
from manage_products.models.product_schemas import Product

client = TestClient(api)


def test_create_product(new_random_product: dict):
    response = client.post("/api/products", json=new_random_product)
    product_response = Product(**response.json())
    assert response.status_code == 201
    assert type(product_response) is Product
    assert product_response.price == new_random_product['price']
    assert product_response.name == new_random_product['name']
    assert product_response.description == new_random_product['description']
