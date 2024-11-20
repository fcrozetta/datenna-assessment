from pydantic import BaseModel, Field


class CustomerbaseSchema(BaseModel):
    name: str
    is_active: bool = True


class CustomerSchema(CustomerbaseSchema):
    key: str = Field(str, alias="_key")
