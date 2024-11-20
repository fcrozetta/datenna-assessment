from fastapi.routing import APIRouter
from repository.arango_repository import ArangoRepository
from schemas.customer_schema import CustomerSchema
from schemas import product_schema as schema

app = APIRouter(prefix="/product", tags=["Product"])

repo = ArangoRepository()


@app.get("/", response_model=list[schema.ProductSchema])
async def list_products(skip: int | None = None, limit: int | None = 10):
    """Return a list of customers"""
    x = repo.get_products(skip, limit)
    return x


@app.post("/", response_model=schema.ProductSchema)
async def add_product(product: schema.ProductBaseSchema):
    result = repo.add_product(product)
    return result


@app.get("/{key}", response_model=schema.ProductSchema)
async def get_product(key: str):
    result = repo.get_product(key)
    return result


@app.get("/{key}/buyers", response_model=list[CustomerSchema])
async def get_product_buyers(key: str):
    result = repo.get_buyers(product_key=key)
    return result
