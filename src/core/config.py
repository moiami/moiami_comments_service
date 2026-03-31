import os


class Config:
    DEBUG = True
    RESOURCE_SERVICE_URL = os.getenv("RESOURCE_SERVICE_URL", "http://resource-service:8000")


config = Config()