import fastapi
import uvicorn

from manage_products.api import products
from manage_products.views import home

api = fastapi.FastAPI()


def configure():
    configure_routing()


def configure_routing():
    api.include_router(home.router)
    api.include_router(products.router)


configure()
if __name__ == "__main__":
    uvicorn.run(api, host="127.0.0.1")
