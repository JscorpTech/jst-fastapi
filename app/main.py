from app import load  # noqa
from app.api.auth.routes import auth
from app.api.v1.routes import root
from fastapi_core.asgi import application

app = application()

app.include_router(root.router)
app.include_router(auth.router)
