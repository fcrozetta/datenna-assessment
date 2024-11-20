from fastapi.routing import APIRouter
from fastapi.responses import Response
from repository.arango_repository import ArangoRepository
from schemas import customer_schema as schema

app = APIRouter(prefix="/customer", tags=["Customer"])

repo = ArangoRepository()


@app.get("/", response_model=list[schema.CustomerSchema])
async def list_customer(skip: int | None = None, limit: int | None = 10):
    """
    list_customer List all customer in given skip/limit window
    """
    x = repo.get_customers(skip, limit)
    return x


@app.post("/", response_model=schema.CustomerSchema)
async def add_customer(customer: schema.CustomerbaseSchema):
    """Add a new Customer"""
    result = repo.add_customer(customer)
    return result


@app.get("/{key}", response_model=schema.CustomerSchema)
async def get_customer(key: str):
    if result := repo.get_customer(key):
        return result
    else:
        return Response(status_code=404)


@app.post("/{customer_key}/purchase/{product_key}")
async def make_purchase(customer_key: str, product_key: str):
    return repo.add_purchase(customer_key=customer_key, product_key=product_key)


@app.get("/{customer_key}/recommendation")
async def get_recommendation(customer_key: str):
    return repo.get_recommendation(customer_key=customer_key)
