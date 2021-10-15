from pathlib import Path
from os.path import abspath
from os.path import join
from os.path import dirname
from os.path import isdir
from os.path import exists


secret_dir = abspath(join(dirname( __file__ ), "..", "..", "secret"))
assert isdir(secret_dir), ("need to have the %s directory (check README)") % (secret_dir)


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    db_url_staging_path = Path(join(secret_dir, "db_url_staging"))
    assert exists(db_url_staging_path), ("need to have the %s file (check README)") % (db_url_staging_path)
    SQLALCHEMY_DATABASE_URI = db_url_staging_path.read_text().strip()
    private_key_path = Path(join(secret_dir, "private_key"))
    assert exists(private_key_path), ("need to have the %s file (check README)") % (private_key_path)
    JWT_PRIVATE_KEY = private_key_path.read_text().strip()


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    db_url_testing_path = Path(join(secret_dir, "db_url_testing"))
    assert exists(db_url_testing_path), ("need to have the %s file (check README)") % (db_url_testing_path)
    SQLALCHEMY_DATABASE_URI = db_url_testing_path.read_text().strip()


config = StagingConfig() # for staging


# Uncomment the following block of code on the production server
"""
class ProductionConfig(Config):
    DEBUG = False
    db_url_production_path = Path(join(secret_dir, "db_url_production"))
    assert exists(db_url_production_path), ("need to have the %s file (check README)") % (db_url_production_path)
    SQLALCHEMY_DATABASE_URI = db_url_production_path.read_text().strip()


config = ProductionConfig() # for production
"""
