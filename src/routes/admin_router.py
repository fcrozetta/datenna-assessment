from fastapi.routing import APIRouter
from schemas.admin_schemas import DBQuery
from services.arango.arango_service import ArangoService

app = APIRouter(prefix="/admin", tags=["Admin"])


@app.get("/force_error")
def force_error():
    """Force error to show in sentry"""
    return 1 / 0


@app.get("/db/truncate")
async def truncate_db():
    db = ArangoService()
    db.truncate()


@app.get("/db/populate")
async def populate_db():
    db = ArangoService()
    db._populate()


@app.post("db/query")
async def query_db(input_query: DBQuery):
    query_str = input_query.query
    service = ArangoService()
    aql = service.get_db().aql
    return list(aql.execute(query_str))
