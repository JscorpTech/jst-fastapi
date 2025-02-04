import logging  # noqa

from tests.conftest import TestingSessionLocal


class TestAuth:

    def setup_method(self):
        self.db = TestingSessionLocal()
        logging.info("run")

    def teardown_method(self):
        self.db.close()

    def test_register(self, client):
        response = client.post(
            "/auth/register",
            json={
                "phone": "998888112319",
                "password": "password",
                "first_name": "John",
                "last_name": "Doe",
            },
        )
        assert response.status_code == 200
