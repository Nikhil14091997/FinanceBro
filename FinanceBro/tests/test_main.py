from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

import warnings
warnings.simplefilter("always")

@pytest.mark.filterwarnings("ignore:.*The 'app' shortcut is now deprecated.*:DeprecationWarning")
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to FinanceBro!"}

