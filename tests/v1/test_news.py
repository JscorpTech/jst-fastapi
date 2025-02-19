import logging  # noqa

from app.db.models import PostModel
from tests.conftest import TestingSessionLocal


class TestNews:

    def setup_method(self):
        self.db = TestingSessionLocal()
        self.post = PostModel(title={"uz": "Test Post"}, content={"uz": "This is a test post."})
        self.db.add(self.post)
        self.db.commit()

    def teardown_method(self):
        self.db.close()

    def test_get_post(self, client):
        response = client.get("/v1/news/post/")
        assert response.status_code == 200
        assert response.json()["status"] is True

    def test_create_post(self, client):
        response = client.post(
            "/v1/news/post",
            json={
                "title": {"uz": "Test Post"},
                "content": {"uz": "This is a test post."},
                "tags": [{"name": "Test Tag"}],
            },
        )
        assert response.status_code == 200
        assert response.json()["status"] is True

    def test_detail_post(self, client):
        response = client.get(f"/v1/news/post/{self.post.id}")
        assert response.status_code == 200
        assert response.json()["status"] is True
