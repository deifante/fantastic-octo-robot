import fastapi

from manage_products.models import product_schemas
from manage_products.models.product import Product
from manage_products.services import product

router = fastapi.APIRouter()


@router.post(
    "/api/products",
    status_code=201,
    response_model=product_schemas.Product,
)
def create_product(product_input: product_schemas.ProductCreate) -> Product:
    return product.create_product(product=product_input)


# TODO: Implement this method
@router.get("/api/products/{product_id}", response_model=product_schemas.Product)
async def get_product(product_id: int):
    raise Exception("get_product endpoint is not implemented")


# TODO: Implement this method
@router.delete("/api/products/{product_id}", response_model=product_schemas.Product)
def delete_product(product_id: int):
    raise Exception("delete_product endpoint is not implemented")


@router.get("/api/products")
async def get_products(
    skip: int = 0,
    limit: int = 5,
):
    return product.get_products(skip=skip, limit=limit)
