import pytest_factoryboy
from users.tests import factories


pytest_factoryboy.register(factories.UserFactory)
