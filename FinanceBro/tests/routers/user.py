from fastapi.testclient import TestClient
from main import app  # Import your FastAPI app
from datetime import datetime

client = TestClient(app)

def test_register_user_success():
    # Test successful user registration
    response = client.post(
        "/register",
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

def test_register_user_invalid_date_format():
    response = client.post(
        "/register",
        json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com",
            "password": "secret",
            "date_of_birth": "2000-01-01", 
            "location_state": "Arizona",
            "location_country": "USA"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid date format. Use MM/DD/YYYY."

def test_register_user_duplicate_email():
    response = client.post(
        "/register",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",  # Duplicate email
            "password": "secret",
            "date_of_birth": "01/01/2000",
            "location_state": "Arizona",
            "location_country": "USA"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "A user with this email already exists."

