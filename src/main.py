from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sentry_sdk
import logging
from config.config import Config
from routes.admin_router import app as admin
from routes.customer_router import app as customer
from routes.product_router import app as product

config = Config()

app = FastAPI(title="Datenna Assessment", version="0.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if config.SENTRY_DSN:
    logging.info("Initializing sentry")
    sentry_sdk.init(
        dsn=config.SENTRY_DSN,
    )


app.include_router(admin)
app.include_router(customer)
app.include_router(product)
