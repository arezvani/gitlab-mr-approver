import os
import sys

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_PATH not in sys.path:
    sys.path.insert(1, ROOT_PATH)

from config import conf

class AppConfig:
    SECRET_KEY = conf.APP_SECRET_KEY
    SQLALCHEMY_DATABASE_URI = conf.DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = conf.DB_POOL_SIZE
    SQLALCHEMY_POOL_TIMEOUT = conf.DB_POOL_TIMEOUT
    SQLALCHEMY_POOL_RECYCLE = conf.DB_POOL_RECYCLE