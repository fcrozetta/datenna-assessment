from pydantic import BaseModel, Field


class ProductBaseSchema(BaseModel):
    name: str
    price: float
    is_active: bool = True


class ProductSchema(ProductBaseSchema):
    key: str = Field(str, alias="_key")
