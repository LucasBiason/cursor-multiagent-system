"""
User Router Tests

Tests for user API endpoints.
"""
import pytest
from fastapi import status


def test_create_user(client):
    """Test creating a user."""
    response = client.post(
        "/api/v1/users/",
        json={
            "email": "test@example.com",
            "name": "Test User",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"
    assert "id" in data


def test_get_user(client):
    """Test getting a user."""
    # Create user first
    create_response = client.post(
        "/api/v1/users/",
        json={
            "email": "test@example.com",
            "name": "Test User",
        },
    )
    user_id = create_response.json()["id"]

    # Get user
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == user_id
    assert data["email"] == "test@example.com"


def test_list_users(client):
    """Test listing users."""
    # Create some users
    for i in range(3):
        client.post(
            "/api/v1/users/",
            json={
                "email": f"user{i}@example.com",
                "name": f"User {i}",
            },
        )

    # List users
    response = client.get("/api/v1/users/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["items"]) >= 3
    assert data["total"] >= 3


def test_update_user(client):
    """Test updating a user."""
    # Create user
    create_response = client.post(
        "/api/v1/users/",
        json={
            "email": "test@example.com",
            "name": "Test User",
        },
    )
    user_id = create_response.json()["id"]

    # Update user
    response = client.patch(
        f"/api/v1/users/{user_id}",
        json={
            "name": "Updated Name",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Updated Name"


def test_delete_user(client):
    """Test deleting a user."""
    # Create user
    create_response = client.post(
        "/api/v1/users/",
        json={
            "email": "test@example.com",
            "name": "Test User",
        },
    )
    user_id = create_response.json()["id"]

    # Delete user
    response = client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify user is inactive
    get_response = client.get(f"/api/v1/users/{user_id}")
    assert get_response.status_code == status.HTTP_200_OK
    assert get_response.json()["is_active"] is False

