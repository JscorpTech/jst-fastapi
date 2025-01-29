import os
from importlib import import_module


class LazySettings(object):
    settings: object = object

    def __init__(self):
        self.settings = import_module(os.getenv("SETTINGS_MODULE"))
        self.__dict__.update(self.settings.__dict__)

    def __getattr__(self, name):
        return getattr(self.settings, name)


settings = LazySettings()
