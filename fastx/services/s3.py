from fastx.conf import settings

# from typing import Any, Union
import boto3  # type: ignore
from botocore.client import BaseClient  # type: ignore


class S3Service:
    connection = None
    _s3_id: str
    _s3_key: str
    _s3_endpoint: str
    _s3_bucket: str

    def __init__(self):
        self._s3_key = settings.S3_KEY
        self._s3_id = settings.S3_ID
        self._s3_endpoint = settings.S3_ENDPOINT
        self._s3_bucket = settings.S3_BUCKET
        super().__init__()

    def get_connection(self) -> BaseClient:
        if S3Service.connection is None:
            S3Service.connection = boto3.client(
                "s3",
                verify=False,
                endpoint_url=self._s3_endpoint,
                aws_access_key_id=self._s3_id,
                aws_secret_access_key=self._s3_key,
            )
        return S3Service.connection

    @property
    def bucket(self) -> str:
        return self._s3_bucket
