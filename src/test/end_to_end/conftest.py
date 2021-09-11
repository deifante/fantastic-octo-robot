import pytest
import random
import faker

random.seed()
fake = faker.Faker()


@pytest.fixture
def new_random_product() -> dict:

    return {"name": fake.word(), "price": random.uniform(1, 100), "description": fake.sentence()}
