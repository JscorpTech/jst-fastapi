from tortoise import Model as TortoiseModel
from tortoise import fields


class Model(TortoiseModel):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-id"]

    def __str__(self) -> str:
        return "Object with id: {}".format(self.id)
