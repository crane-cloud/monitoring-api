import os


class Base:
    """ base config """

    # main
    SECRET_KEY = os.getenv("FLASK_APP_SECRET")
    FLASK_APP_SALT = os.getenv("FLASK_APP_SALT")
    PRODUCT_BASE_URL = os.getenv('PRODUCT_BASE_URL')


class Development(Base):
    """ development config """

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URI", "postgresql:///cranecloud")


class Testing(Base):
    """ test environment config """

    TESTING = True
    DEBUG = True
    # use a separate db
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "TEST_DATABASE_URI") or "postgresql:///cranecloud_test_db"


class Staging(Base):
    """ Staging config """

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    MONGO_URI = os.getenv("MONGO_URI")


class Production(Base):
    """ production config """

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")


app_config = {"development": Development, "testing": Testing,
              "staging": Staging, "production": Production}
