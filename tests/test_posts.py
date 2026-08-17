import pytest
import requests
from datetime import datetime


BASE_URL = "http://localhost:8000/api"


class TestPostsAPI:
    """Test suite for Posts API endpoints"""

    @pytest.fixture
    def setup(self):
        """Setup test data"""
        self.post_data = {
            "title": "Test Post",
            "content": "This is a test post content",
            "author": "Test Author"
        }
        yield
        # Cleanup if needed

    def test_get_all_posts(self):
        """Test retrieving all posts"""
        response = requests.get(f"{BASE_URL}/posts")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_post_by_id(self):
        """Test retrieving a specific post by ID"""
        post_id = 1
        response = requests.get(f"{BASE_URL}/posts/{post_id}")
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            data = response.json()
            assert "id" in data
            assert data["id"] == post_id

    def test_create_post(self, setup):
        """Test creating a new post"""
        response = requests.post(f"{BASE_URL}/posts", json=self.post_data)
        assert response.status_code in [201, 200]
        data = response.json()
        assert "id" in data
        assert data["title"] == self.post_data["title"]
        assert data["content"] == self.post_data["content"]

    def test_create_post_missing_fields(self):
        """Test creating a post with missing required fields"""
        invalid_data = {"title": "Test"}
        response = requests.post(f"{BASE_URL}/posts", json=invalid_data)
        assert response.status_code in [400, 422]

    def test_update_post(self, setup):
        """Test updating an existing post"""
        post_id = 1
        updated_data = {
            "title": "Updated Title",
            "content": "Updated content"
        }
        response = requests.put(f"{BASE_URL}/posts/{post_id}", json=updated_data)
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            data = response.json()
            assert data["title"] == updated_data["title"]

    def test_delete_post(self):
        """Test deleting a post"""
        post_id = 1
        response = requests.delete(f"{BASE_URL}/posts/{post_id}")
        assert response.status_code in [200, 204, 404]

    def test_get_post_invalid_id(self):
        """Test retrieving post with invalid ID"""
        response = requests.get(f"{BASE_URL}/posts/invalid")
        assert response.status_code in [400, 404]

    def test_create_post_empty_title(self):
        """Test creating post with empty title"""
        invalid_data = {
            "title": "",
            "content": "Some content",
            "author": "Author"
        }
        response = requests.post(f"{BASE_URL}/posts", json=invalid_data)
        assert response.status_code in [400, 422]

    def test_posts_response_schema(self):
        """Test that posts response has correct schema"""
        response = requests.get(f"{BASE_URL}/posts")
        if response.status_code == 200:
            posts = response.json()
            if posts:
                post = posts[0]
                required_fields = ["id", "title", "content"]
                for field in required_fields:
                    assert field in post
