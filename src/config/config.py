import os


class Config:
    def __init__(self):
        self.DEBUG = bool(os.getenv("DEBUG", "0"))
        self.SENTRY_DSN = os.getenv("SENTRY_DSN", None)
