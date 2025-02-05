import logging  # noqa

from fastapi.testclient import TestClient
from tests.base import BaseTest
import pytest
from app.db.models import OtpModel
from fastx.services.redis import redis


@pytest.mark.asyncio
class TestAuth(BaseTest):
    code: str
    phone: str

    def setup_method(self):
        super().setup_method()
        self.code = "111111"
        self.phone = "998888112309"
        self._create_user()

    def test_register(self, client: TestClient):
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

    def test_login(self, client: TestClient):
        response = client.post("/auth/login", json={"phone": "998943990509", "password": "Samandar001@"})
        assert response.status_code == 200
        assert response.json()["status"] is True

    async def test_change_password(self, client: TestClient):
        await self.create_token()
        response = client.post(
            "/auth/change-password",
            json={"old_password": "Samandar001@", "new_password": "password"},
            headers=await self.auth_headers(),
        )
        assert response.status_code == 200
        assert response.json()["status"] is True

    async def test_send_code(self, client: TestClient):
        response = client.post("/auth/resend-code", json={"phone": "998888112309"})
        assert response.status_code == 200
        assert response.json()["status"] is True

    async def test_reset_password(self, client: TestClient):
        otp = OtpModel(phone=self.phone, otp=self.code)
        self.db.add(otp)
        self.db.commit()
        self.db.refresh(otp)
        response = client.post("/auth/reset-password", json={"phone": self.phone, "code": self.code})
        assert response.status_code == 200
        assert response.json()["status"] is True

    async def test_reset_password_confirm(self, client: TestClient):
        token = "token"
        redis.set_key("reset-password:{}".format(token), self._phone)
        response = client.post("/auth/reset-password/confirm", json={"token": token, "password": "Samandar001@"})
        assert response.status_code == 200
        assert response.json()["status"] is True

    async def test_update(self, client: TestClient):
        response = client.patch("/auth/update", json={"first_name": "Samandar"}, headers=await self.auth_headers())
        assert response.status_code == 200
        assert response.json()["status"] is True

    async def test_update_avatar(self, client: TestClient):
        with open("storage/image.png", "rb") as file:
            response = client.post(
                "/auth/update/avatar",
                files={"file": ("image.png", file, "image/png")},
                headers=await self.auth_headers(),
            )

        assert response.status_code == 200
        assert response.json()["status"] is True

    async def test_me(self, client: TestClient):
        response = client.get("/auth/me", headers=await self.auth_headers())
        assert response.status_code == 200
        assert response.json()["status"] is True
