from tests.mock_dependencies import MockSession

from fastapi.testclient import TestClient
from main import app
from datetime import datetime

from unittest.mock import patch


client = TestClient(app)

@patch('dependencies.SessionLocal', return_value=MockSession())
def test_register_user_success(mock_get_db):
    mock_get_db.add.return_value = None  
    mock_get_db.commit.return_value = None  
    mock_get_db.refresh.return_value = None 

    response = client.post(
        "/user/register",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "secret",
            "date_of_birth": "01/01/2000",
            "location_state": "Arizona",
            "location_country": "USA"
        }
    )
    assert response.status_code == 201
    assert response.json()["status_code"] == 201
    assert response.json()["message"] == "User registered successfully"
    assert "data" in response.json()
    assert response.json()["data"]["email"] == "john.doe@example.com"