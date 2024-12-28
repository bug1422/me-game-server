from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    MONGODB_SETTINGS = {
        "db": os.getenv("MONGO_DB", ""),
        "host": os.getenv("MONGO_HOST", ""),
        "port": os.getenv("MONGO_PORT", 27017),
        "username": os.getenv("MONGO_USER"),
        "password": os.getenv("MONGO_PASS"),
    }


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass
