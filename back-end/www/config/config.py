from pathlib import Path
from os.path import abspath
from os.path import join
from os.path import dirname
from os.path import isdir
from os.path import exists
import os


secret_dir = abspath(join(dirname(__file__), "..", "..", "secret"))
assert isdir(secret_dir), ("need to have the %s directory (check README)") % (
    secret_dir
)

# Determine which environment to use
FLASK_ENV = os.environ.get("FLASK_ENV", "production")


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    private_key_path = Path(join(secret_dir, "private_key"))
    assert exists(private_key_path), ("need to have the %s file (check README)") % (
        private_key_path
    )
    JWT_PRIVATE_KEY = private_key_path.read_text().strip()
    # Database URI will be set by subclasses
    SQLALCHEMY_DATABASE_URI = None


def get_staging_config():
    """Get staging configuration - only loads if staging files exist"""

    class StagingConfig(Config):
        DEVELOPMENT = True
        DEBUG = True
        db_url_staging_path = Path(join(secret_dir, "db_url_staging"))
        assert exists(db_url_staging_path), (
            "need to have the %s file (check README)"
        ) % (db_url_staging_path)
        SQLALCHEMY_DATABASE_URI = db_url_staging_path.read_text().strip()

    return StagingConfig()


def get_development_config():
    """Get development configuration - only loads if staging files exist"""

    class DevelopmentConfig(Config):
        DEVELOPMENT = True
        DEBUG = True
        db_url_staging_path = Path(join(secret_dir, "db_url_staging"))
        assert exists(db_url_staging_path), (
            "need to have the %s file (check README)"
        ) % (db_url_staging_path)
        SQLALCHEMY_DATABASE_URI = db_url_staging_path.read_text().strip()

    return DevelopmentConfig()


def get_testing_config():
    """Get testing configuration - only loads if testing files exist"""

    class TestingConfig(Config):
        TESTING = True
        db_url_testing_path = Path(join(secret_dir, "db_url_testing"))
        assert exists(db_url_testing_path), (
            "need to have the %s file (check README)"
        ) % (db_url_testing_path)
        SQLALCHEMY_DATABASE_URI = db_url_testing_path.read_text().strip()

    return TestingConfig()


def get_production_config():
    """Get production configuration - only loads if production files exist"""

    class ProductionConfig(Config):
        DEBUG = False
        db_url_production_path = Path(join(secret_dir, "db_url_production"))
        assert exists(db_url_production_path), (
            "need to have the %s file (check README)"
        ) % (db_url_production_path)
        SQLALCHEMY_DATABASE_URI = db_url_production_path.read_text().strip()

    return ProductionConfig()


# Select config based on environment
if FLASK_ENV == "testing":
    config = get_testing_config()
elif FLASK_ENV == "development":
    config = get_development_config()
elif FLASK_ENV == "staging":
    config = get_staging_config()
else:
    # Default to production
    config = get_production_config()
