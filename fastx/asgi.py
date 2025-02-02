from fastapi import FastAPI

import fastx


def application() -> FastAPI:
    return fastx.setup()
