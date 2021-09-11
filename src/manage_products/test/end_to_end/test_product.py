from fastapi.testclient import TestClient

from manage_products.main import api

client = TestClient(api)


def test_create_product():
    assert True
