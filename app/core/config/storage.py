from app.core.env import env

S3_ID: str = env.str("S3_ID")
S3_KEY: str = env.str("S3_KEY")
S3_ENDPOINT: str = env.str("S3_ENDPOINT")
S3_BUCKET: str = env.str("S3_BUCKET")
S3_URL = env.str("S3_URL", "http://146.0.75.247:2300/fastx")
