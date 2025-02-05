import logging  # noqa
from app.api.auth.services.auth import create_token
from app.db.models import UserModel
from passlib.hash import bcrypt
from tests.conftest import TestingSessionLocal
from sqlalchemy.orm import Session


class BaseTest:
    user: UserModel
    token: str
    db: Session
    _phone: str = "998943990509"

    def setup_method(self):
        self.db = TestingSessionLocal()

    def teardown_method(self):
        self.db.close()

    async def auth_headers(self) -> dict:
        return {"Authorization": f"Bearer {await self.create_token()}"}

    def _create_user(self):
        self.user = UserModel(
            phone=self._phone, password=bcrypt.hash("Samandar001@"), first_name="Samandar", last_name="Azamov"
        )
        self.db.add(self.user)
        self.db.commit()
        self.db.refresh(self.user)

    async def create_token(self):
        self.token = (await create_token(self.user))["access_token"]
        return self.token
