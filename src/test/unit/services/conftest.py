import datetime
import random

import pytest
import faker

random.seed()
fake = faker.Faker()


from manage_products.models.product import Product


@pytest.fixture()
def random_product() -> Product:
    return Product(
        id=random.randint(1, 100),
        name=fake.word(),
        price=random.uniform(1, 100),
        description=fake.sentence(),
        views=random.randint(0, 100),
        is_deleted=False,
        created_date=datetime.datetime.utcnow(),
    )
