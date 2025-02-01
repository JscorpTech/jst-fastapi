from fastapi import Request
from pyinstrument import Profiler

from fastapi_core.conf import settings
from fastapi_core.utils.translation import set_language


async def profiler_middleware(request, call_next):
    profiler = Profiler()
    profiler.start()
    response = await call_next(request)
    profiler.stop()
    with open("profiler.html", "w") as f:
        f.write(profiler.output_html())
    return response


async def translation_middleware(request: Request, call_next):
    language = request.headers.get("Accept-Language", settings.LANGUAGE)
    if language in settings.LANGUAGES:
        set_language(language)
    response = await call_next(request)
    return response
