import pytest
from rest_framework.test import APIClient


pytest_plugins = [
    "users.tests.fixtures",
    "users.tests.factories",
]


@pytest.fixture
def api_client():
    return APIClient()
