from celery import Celery
from .load import * # noqa
from fastx.conf import  settings


app = Celery('tasks', broker=settings.REDIS_URL, backend=settings.REDIS_URL)
