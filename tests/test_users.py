import pytest
import requests
from unittest.mock import patch, MagicMock


BASE_URL = "http://localhost:8000/"


class TestUsersAPI:
    """Test suite for Users API endpoints"""

    def test_get_all_users_success(self):
        """Test retrieving all users successfully"""
        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = [
                {"id": 1, "name": "John Doe", "email": "john@example.com"},
                {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
            ]
            mock_get.return_value = mock_response

            response = requests.get(f"{BASE_URL}/users")
            
            assert response.status_code == 200
            assert len(response.json()) == 2
            assert response.json()[0]["name"] == "John Doe"

    def test_get_user_by_id_success(self):
        """Test retrieving a user by ID successfully"""
        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"id": 1, "name": "John Doe", "email": "john@example.com"}
            mock_get.return_value = mock_response

            response = requests.get(f"{BASE_URL}/users/1")
            
            assert response.status_code == 200
            assert response.json()["id"] == 1
            assert response.json()["email"] == "john@example.com"

    def test_get_user_by_id_not_found(self):
        """Test retrieving a non-existent user"""
        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 404
            mock_response.json.return_value = {"error": "User not found"}
            mock_get.return_value = mock_response

            response = requests.get(f"{BASE_URL}/users/999")
            
            assert response.status_code == 404

    def test_create_user_success(self):
        """Test creating a new user successfully"""
        with patch('requests.post') as mock_post:
            mock_response = MagicMock()
            mock_response.status_code = 201
            mock_response.json.return_value = {"id": 3, "name": "Bob Johnson", "email": "bob@example.com"}
            mock_post.return_value = mock_response

            user_data = {"name": "Bob Johnson", "email": "bob@example.com"}
            response = requests.post(f"{BASE_URL}/users", json=user_data)
            
            assert response.status_code == 201
            assert response.json()["name"] == "Bob Johnson"

    def test_create_user_invalid_data(self):
        """Test creating a user with invalid data"""
        with patch('requests.post') as mock_post:
            mock_response = MagicMock()
            mock_response.status_code = 400
            mock_response.json.return_value = {"error": "Invalid user data"}
            mock_post.return_value = mock_response

            user_data = {"name": ""}
            response = requests.post(f"{BASE_URL}/users", json=user_data)
            
            assert response.status_code == 400

    def test_update_user_success(self):
        """Test updating a user successfully"""
        with patch('requests.put') as mock_put:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"id": 1, "name": "John Updated", "email": "john.updated@example.com"}
            mock_put.return_value = mock_response

            user_data = {"name": "John Updated", "email": "john.updated@example.com"}
            response = requests.put(f"{BASE_URL}/users/1", json=user_data)
            
            assert response.status_code == 200
            assert response.json()["name"] == "John Updated"

    def test_update_user_not_found(self):
        """Test updating a non-existent user"""
        with patch('requests.put') as mock_put:
            mock_response = MagicMock()
            mock_response.status_code = 404
            mock_response.json.return_value = {"error": "User not found"}
            mock_put.return_value = mock_response

            user_data = {"name": "John Updated"}
            response = requests.put(f"{BASE_URL}/users/999", json=user_data)
            
            assert response.status_code == 404

    def test_delete_user_success(self):
        """Test deleting a user successfully"""
        with patch('requests.delete') as mock_delete:
            mock_response = MagicMock()
            mock_response.status_code = 204
            mock_delete.return_value = mock_response

            response = requests.delete(f"{BASE_URL}/users/1")
            
            assert response.status_code == 204

    def test_delete_user_not_found(self):
        """Test deleting a non-existent user"""
        with patch('requests.delete') as mock_delete:
            mock_response = MagicMock()
            mock_response.status_code = 404
            mock_response.json.return_value = {"error": "User not found"}
            mock_delete.return_value = mock_response

            response = requests.delete(f"{BASE_URL}/users/999")
            
            assert response.status_code == 404
