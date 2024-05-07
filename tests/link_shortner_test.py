from fastapi.testclient import TestClient
from src.main import app
import json
import pytest
from pymongo import MongoClient

client = TestClient(app)


@pytest.fixture(scope="module")
def test_db():
    # Set up mock database
    client = MongoClient("mongodb://localhost:27017/")
    test_db = client["test_database"]
    yield test_db
    # Teardown: clean up mock database after tests
    test_db["link_collection"].drop()
    test_db["users_collection"].drop()
    client.close()





def test_routes_with_mock_db(test_db):
    # Register a user
    register_response = client.post("/register", json={"email": "test@example.com", "password": "testpassword"})
    assert register_response.status_code == 201

    # Obtain an access token
    token_response = client.post("/token", data={"username": "test@example.com", "password": "testpassword"})
    assert token_response.status_code == 200
    token_data = token_response.json()
    access_token = token_data["access_token"]

    # Test create_short_link with authentication
    response = client.post("/shorten/", json={"link": "https://example.com"}, headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert "shortened_link" in response.json()

    response = client.post("/shorten/", json={"link": "invalid-url"}, headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 400

    # Test redirect_to_path
    shortened_link_code = "your_shortened_link_code"
    test_db["link_collection"].insert_one(
        {
            "link": "https://example.com",
            "shortned_link": shortened_link_code,
            "created_date": "2024-05-07T12:00:00",
            "user_id": "user_id_here",
        }
    )

    response = client.get(f"/{shortened_link_code}")
    assert response.status_code == 302

    response = client.get("/non_existent_shortened_link")
    assert response.status_code == 404