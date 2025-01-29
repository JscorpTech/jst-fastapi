from fastapi_core.db import Model, fields


class OtpModel(Model):
    phone = fields.CharField(max_length=255)
    otp = fields.IntField(max_length=255)

    class Meta:
        table = "otps"
