import os


class Config:
    DEBUG = True
    RESOURCE_SERVICE_URL = os.getenv(
        "RESOURCE_SERVICE_URL", "localhost:8000")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = Config()
