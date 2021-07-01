import os

class Config():
    DEBUG = False
    TESTING = False
    user = os.environ["POSTGRES_USER"]
    password = os.environ["POSTGRES_PASSWORD"]
    hostname = os.environ["POSTGRES_HOSTNAME"]
    port = os.environ["POSTGRES_PORT"]
    database = os.environ["APPLICATION_DB"]

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{user}:{password}@{hostname}:{port}/{database}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Production configuration"""
    pass


class ProductionConfig(Config):
    """Production configuration"""
    pass


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SERVER_NAME = 'localhost:5000'
    APPLICATION_ROOT = '/'
