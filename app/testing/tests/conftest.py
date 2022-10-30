import pytest

from database.models.models import db
from testing.helpers.mock_db import *

# By declaring the fixture with autouse=True, it will be automatically invoked 
# for each test function defined in the same module.
@pytest.fixture(autouse=True)
def run_before_and_after():
    # Code that will run before each test
    db.drop_all_tables(with_all_data=True)
    db.create_tables()
    users()
    robots()
    matches()
    # A test function will be ran at this point
    yield
    # Code that will run after each test
    db.drop_all_tables(with_all_data=True)
    