from fastapi import FastAPI
import fastapi_core


def application() -> FastAPI:
    return fastapi_core.setup()
