from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    id: int
    phone: str | int
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    email: str | None = None

    class Config:
        from_attributes = True
