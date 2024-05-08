from fastapi.testclient import TestClient
from src.main import app
import json
import pytest
from pymongo import MongoClient
import pytest
from datetime import datetime
from src.link_shortener.models import Link
from pydantic import ValidationError
import pytest
from src.link_shortner.utils import is_valid_url, link_validate


@pytest.mark.parametrize(
    "url, expected",
    [
        ("http://example.com", True),
        ("https://example.com", True),
        ("http://www.example.com", True),
        ("https://www.example.com", True),
        ("http://example.com/path", True),
        ("https://example.com/path", True),
        ("http://example.com/path?query=param", True),
        ("https://example.com/path?query=param", True),
        ("http://example.com/path#fragment", True),
        ("https://example.com/path#fragment", True),
        ("example.com", True),
        ("http://", False),
        ("https://", False),
        ("http://example", False),
        ("https://example", False),
        ("http://example.", False),
        ("https://example.", False),
        ("http://.com", False),
        ("https://.com", False),
    ],
)
def test_is_valid_url(url, expected):
    assert is_valid_url(url) == expected


def test_link_validate():
    assert link_validate("example.com") == "http://example.com"
    assert link_validate("http://example.com") == "http://example.com"
    assert link_validate("https://example.com") == "https://example.com"


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


def test_link_model_validation():
    # Valid data
    valid_data = {
        "link": "https://example.com",
        "shortned_link": "abc123",
        "created_date": datetime.now(),
        "clicked": 0,
        "user_id": None,
    }

    # Test valid data
    link = Link(**valid_data)
    assert link.link == valid_data["link"]
    assert link.shortned_link == valid_data["shortned_link"]
    assert link.created_date == valid_data["created_date"]
    assert link.clicked == valid_data["clicked"]
    assert link.user_id == valid_data["user_id"]

    # Test link length validation
    with pytest.raises(ValidationError) as exc_info:
        Link(
            link="https://" + "a" * 1001,
            shortned_link="abc123",
            created_date=datetime.now(),
        )
    assert "Link must be at most 500 characters long" in str(exc_info.value)


def test_routes_with_mock_db(test_db):
    # Register a user
    register_response = client.post(
        "/register", json={"email": "test@example.com", "password": "testpassword"}
    )
    assert register_response.status_code == 201

    # Obtain an access token
    token_response = client.post(
        "/token", data={"username": "test@example.com", "password": "testpassword"}
    )
    assert token_response.status_code == 200
    token_data = token_response.json()
    access_token = token_data["access_token"]

    # Test create_short_link with authentication
    response = client.post(
        "/shorten/",
        json={"link": "https://example.com"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    assert "shortened_link" in response.json()

    response = client.post(
        "/shorten/",
        json={"link": "invalid-url"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
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
