import sys, pathlib
from fastapi.testclient import TestClient
from sqlalchemy import text
from app.main import app
from app.database import engine
import pytest

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))


@pytest.fixture
def client():
    """Fixture to provide a test client for FastAPI."""
    return TestClient(app)


def setup_module():
    # Clean users table before tests run
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE"))


def test_create_and_get_user(client):
    payload = {
        "username": "alice",
        "email": "alice@example.com",
        "password": "Pass123!",
    }
    r = client.post("/users/", json=payload)
    assert r.status_code == 201
    user_id = r.json()["id"]

    r2 = client.get(f"/users/{user_id}")
    assert r2.status_code == 200
    data = r2.json()
    assert data["username"] == "alice"
    assert "password_hash" not in data


def test_duplicate_user(client):
    payload = {"username": "bob", "email": "bob@example.com", "password": "x"}
    assert client.post("/users/", json=payload).status_code == 201
    r = client.post("/users/", json=payload)
    assert r.status_code == 409


def test_get_nonexistent_user_returns_404(client):
    response = client.get("/users/999999")  # Use a user ID that doesn't exist
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
