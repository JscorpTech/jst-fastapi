import os

DATABSE_ENGINE: str = os.getenv("DATABASE_ENGINE")
DATABSE_USER: str = os.getenv("DATABASE_USER")
DATABSE_PASSWORD: str = os.getenv("DATABASE_PASSWORD")
DATABSE_HOST: str = os.getenv("DATABASE_HOST")
DATABSE_NAME: str = os.getenv("DATABASE_NAME")
DATABSE_PORT: str | int = os.getenv("DATABASE_PORT")
DATABASE_TEST_NAME: str = os.getenv("DATABASE_TEST_NAME")
DATABASE_URL: str = (
    f"{DATABSE_ENGINE}://{DATABSE_USER}:{DATABSE_PASSWORD}@{DATABSE_HOST}:{DATABSE_PORT}/{DATABSE_NAME}"  # noqa
)
TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": [
                "app.db.models",
                "aerich.models",
            ],
            "default_connection": "default",
        },
    },
}
