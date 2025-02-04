from typing import List, Literal, TypeAlias

import magic
from fastapi import UploadFile

from fastx.exceptions import APIException

_IMAGE_MIMES: TypeAlias = Literal["image/png", "image/jpg", "image/jpeg"]
_VIDEO_MIMES: TypeAlias = Literal["video/mp4"]
_AUDIO_MIMES: TypeAlias = Literal["audio/mp3"]

_MIMES: TypeAlias = _IMAGE_MIMES | _AUDIO_MIMES | _VIDEO_MIMES


async def validate_mine(
    file: UploadFile, mimes: List[_MIMES], raise_exception: bool = True, field_name: str = "file"
) -> bool:
    mime = magic.Magic(mime=True)
    file_type = mime.from_buffer(await file.read(2048))
    if file_type not in mimes:
        if raise_exception:
            raise APIException(APIException.VALIDATION_ERROR, 400, data={field_name: "🤨 File mime type not allowed"})
        return False
    return True
