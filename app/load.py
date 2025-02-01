import os

from app.core.env import env  # noqa

os.environ.setdefault("SETTINGS_MODULE", "app.core.settings.local")
