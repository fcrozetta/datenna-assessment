import logging
import os
from arango import ArangoClient
from arango.database import StandardDatabase


class ArangoConfig:
    def __init__(self) -> None:
        self.host = os.getenv("ARANGO_URL", "http://arangodb:8529")
        self.username = os.getenv("ARANGO_USER", "root")
        self.password = os.getenv("ARANGO_PASSWORD", "root")
        self.database = os.getenv("ARANGO_DATABASE", "_system")
        self.node_collections = ["customers", "products"]
        self.edge_collections = ["purchases"]
        self.graph = os.getenv("ARANGO_GRAPH", "purchasesGraph")

    def get_client_config(self):
        return {"hosts": self.host}


class ArangoService:
    config = ArangoConfig()

    def __init__(self) -> None:
        self.client = ArangoClient(**self.config.get_client_config())
        self._initialize_db()

    def _load_aql(self, name: str) -> str:
        with open(name) as f:
            return "\n".join(f.readlines())

    def _initialize_db(self):
        db = self.get_db()
        populate = False
        for collection in self.config.node_collections:
            if not db.has_collection(collection):
                db.create_collection(collection)
                populate = True

        for edges in self.config.edge_collections:
            if not db.has_collection(edges):
                db.create_collection(edges, edge=True)
                populate = True

        if not db.has_graph(self.config.graph):
            graph = db.create_graph(self.config.graph)
            # This has to be changed in case of more edges
            graph.create_edge_definition(
                edge_collection=self.config.edge_collections[0],
                from_vertex_collections=[self.config.node_collections[0]],
                to_vertex_collections=[self.config.node_collections[1]],
            )

        if populate:
            self._populate()

    def _populate(self):
        self.truncate()
        self.execute("src/aql/populate_customers_product.aql")
        self.execute("src/aql/populate_purchases.aql")

    def get_db(self) -> StandardDatabase:
        return self.client.db(
            self.config.database,
            username=self.config.username,
            password=self.config.password,
        )

    def get_graph(self):
        return self.get_db().graph(self.config.graph)

    def truncate(self):
        db = self.get_db()
        for col in self.config.node_collections + self.config.edge_collections:
            db.collection(col).truncate()

    def execute(self, name: str, binds: dict | None = None):
        query = self._load_aql(name)
        # For some reason, loading the aql property is breaking the editor parsing
        aql = self.get_db().aql
        try:
            response = aql.execute(query, bind_vars=binds)
        except Exception as e:
            logging.exception("Could not Execute query", query=query, binds=binds)
            raise e
        return list(response)
