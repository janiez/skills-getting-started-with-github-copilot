from copy import deepcopy
import pytest
from fastapi.testclient import TestClient

from src.app import app, activities

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    # Take a snapshot of the current activities and restore after each test
    original = deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)
