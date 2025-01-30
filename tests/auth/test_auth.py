import logging  # noqa


class TestAuth:

    def setup_method(self):
        logging.info("run")

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
