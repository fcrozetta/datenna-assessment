import logging
from venv import logger
from arango.collection import StandardCollection
from services.arango.arango_service import ArangoService
from schemas import customer_schema, product_schema


class ArangoRepository:
    service = ArangoService()

    def __init__(self) -> None:
        self.customers_collection: StandardCollection = (
            self.service.get_db().collection(self.service.config.node_collections[0])
        )
        self.products_collection: StandardCollection = self.service.get_db().collection(
            self.service.config.node_collections[1]
        )
        self.purchases_collection: StandardCollection = (
            self.service.get_db().collection(self.service.config.edge_collections[0])
        )

    def has_customer(self, customer_key: str) -> bool:
        return self.customers_collection.has(customer_key)

    def has_product(self, product_key: str) -> bool:
        return self.products_collection.has(product_key)

    def get_customer(self, key: str):
        if result := self.customers_collection[key]:
            return result[0]
        else:
            return None

    def get_customers(self, skip: int | None, limit: int | None):
        if result := list(self.customers_collection.all(skip=skip, limit=limit)):
            return result
        else:
            return None

    def add_customer(self, customer: customer_schema.CustomerbaseSchema):
        c = customer.model_dump()
        c["_key"] = customer.name
        try:
            self.customers_collection.insert(c)
        except Exception as e:
            logging.exception("Could not Add customer into DB")
            raise e
        return self.customers_collection[customer.name]

    def get_product(self, key: str):
        if result := self.products_collection[key]:
            return result
        else:
            return None

    def get_products(self, skip: int | None, limit: int | None):
        if result := list(self.products_collection.all(skip=skip, limit=limit)):
            return result
        else:
            return None

    def add_product(self, product: product_schema.ProductBaseSchema):
        p = product.model_dump()
        p["_key"] = product.name
        try:
            self.products_collection.insert(p)
        except Exception as e:
            logger.exception("Could not add product to DB")
            raise e
        return self.products_collection[product.name]

    def add_purchase(self, customer_key: str, product_key: str, weight: int = 0.5):
        if not self.has_customer(customer_key) or not self.has_product(product_key):
            raise Exception("Customer/Product does not exist")
        edge = {
            "_from": f"{self.service.config.node_collections[0]}/{customer_key}",
            "_to": f"{self.service.config.node_collections[1]}/{product_key}",
            "weight": weight,
        }
        try:
            self.purchases_collection.insert(edge)
        except Exception as e:
            logger.exception("Could not add edge into DB")
            raise e
        return

    def get_recommendation(self, customer_key: str):
        return self.service.execute(
            "src/aql/get_products_recommendation.aql",
            {
                "targetCustomer": f"{self.service.config.node_collections[0]}/{customer_key}"
            },
        )

    def get_buyers(self, product_key: str):
        bind_vars = {
            "product_key": f"{self.service.config.node_collections[1]}/{product_key}"
        }
        return self.service.execute("src/aql/get_who_bought.aql", bind_vars)
