import os
from importlib import import_module


class LazySettings(object):
    def __init__(self):
        settings = import_module(os.getenv("SETTINGS_MODULE"))
        self.__dict__.update(settings.__dict__)

    def __getattr__(self, name):
        return getattr(self, name)


settings = LazySettings()
