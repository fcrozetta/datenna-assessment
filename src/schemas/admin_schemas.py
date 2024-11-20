from pydantic import BaseModel


class DBQuery(BaseModel):
    query: str
