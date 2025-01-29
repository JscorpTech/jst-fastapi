from app.core.env import env

JWT_CONFIG = {
    "ACCESS_TOKEN_EXPIRE_MINUTES": env.int("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 30),
    "REFRESH_TOKEN_EXPIRE_MINUTES": env.int(
        "JWT_REFRESH_TOKEN_EXPIRE_MINUTES", 60 * 24 * 7
    ),
    "ALGORITHM": env.str("JWT_ALGORITHM", "HS256"),
    "SECRET": env.str("JWT_SECRET", "secret"),
}
