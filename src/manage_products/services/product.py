from typing import List, Optional

from manage_products.db import sqlite
from manage_products.models.product import Product
from manage_products.models.product_schemas import ProductCreate


def create_product(product: ProductCreate) -> Product:
    query = """
    INSERT INTO products (name, price, description)
    VALUES (?, ?, ?)
    """
    params = (product.name, product.price, product.description)
    new_id = sqlite.write(query, params, lastrowid=True)
    return Product(
        name=product.name,
        price=product.price,
        description=product.description,
        views=0,
        id=new_id,
        is_deleted=False,
    )


# TODO: Implement this method
def get_product(product_id: int) -> Optional[Product]:
    raise Exception("get_product service is not implemented")


# TODO: Implement this method
def delete_product(product_id: int) -> Product:
    raise Exception("delete_product service is not implemented")


def get_products(skip: int = 0, limit: int = 5) -> List[Product]:
    query = """
    SELECT id, name, price, description, views, is_deleted, created_date
    FROM products
    WHERE is_deleted == 0
    ORDER BY views DESC
    LIMIT ?
    OFFSET ?"""
    params = (limit, skip)
    results = sqlite.read(query, params)
    if results:
        return [_convert_to_product(result) for result in results]
    return []


def _convert_to_product(item: dict) -> Product:
    return Product(
        id=item["id"],
        name=item["name"],
        price=item["price"],
        description=item["description"],
        views=item["views"],
        is_deleted=bool(item["is_deleted"]),
        created_date=item["created_date"],
    )
