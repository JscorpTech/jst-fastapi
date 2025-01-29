from fastapi_core.db import Model, fields


class UserModel(Model):
    phone = fields.CharField(max_length=255)
    password = fields.CharField(max_length=255)
    first_name = fields.CharField(max_length=255)
    last_name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "users"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class UserTokenModel(Model):
    user = fields.ForeignKeyField("models.UserModel", related_name="tokens")
    token = fields.CharField(max_length=255)

    class Meta:
        table = "user_tokens"
