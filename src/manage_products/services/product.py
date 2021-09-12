from typing import List, Optional

from manage_products.db import sqlite
from manage_products.models.currency_conversion import DEFAULT_CURRENCY
from manage_products.models.product import Product
from manage_products.models.product_schemas import ProductCreate
from manage_products.services.currency import convert_product_currency


class ProductServiceException(Exception):
    pass


def view_product(product_id: int, currency: str = None) -> Product:
    product = get_product(product_id)
    product.views += 1
    update_product(product)
    if currency and currency != DEFAULT_CURRENCY:
        product = convert_product_currency(product, currency)
    return product


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


def get_product(product_id: int) -> Product:
    query = """
    SELECT id, name, price, description, views, is_deleted, created_date
    FROM products
    WHERE is_deleted == 0
    AND id = ?
    """
    params = (product_id,)
    result = sqlite.read(query=query, params=params)
    if result and len(result) == 1:
        return _convert_to_product(result[0])
    else:
        raise ProductServiceException(f"Unable to get product with id: {product_id}")


def update_product(product: Product):
    query = """
    UPDATE products
    SET name = ?, price = ?, description = ?, views = ?, is_deleted = ?
    WHERE id = ?
    """
    params = (product.name, product.price, product.description, product.views, product.is_deleted, product.id)
    sqlite.write(query=query, params=params)


def delete_product(product_id: int) -> Product:
    product = get_product(product_id)
    product.is_deleted = True
    update_product(product)
    return product


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
