import os
import json
import logging


APP_SECRET_KEY = 'D0ukrk87vh<]IgDYDowsyI]-jVLyX,&0'

# Log
LOG_LEVEL = {
    'webservice': logging.INFO,
    'base': logging.DEBUG,
}
LOG_FORMAT = {
    'webservice': '[%(asctime)s] [%(remote_addr)s] [%(user_agent)s] [%(caller_module)s] [%(method)s] [%(status_code)s] [%(path)s] [%(caller_class)s.%(caller_func)s] [%(levelname)s]: %(message)s',
    'base': '[%(asctime)s] [base] [%(levelname)s]: %(message)s',
}
MASK_FIELDS = ['password']

# Gitlab
GITLAB_URL = os.environ.get("GITLAB_URL", "http://185.60.136.53")
GITLAB_TOKEN = os.environ.get("GITLAB_TOKEN", "glpat-FbyDf7R5JezLx18Kx1s5")
GITLAB_WEBHOOK_TOKEN = os.environ.get("GITLAB_WEBHOOK_TOKEN", "")

# Database
DB_USERNAME = os.environ.get('DB_USERNAME', 'postgres')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'SAra%40131064')
DB_HOST = os.environ.get('DB_HOST', '185.60.136.53')
DB_PORT = os.environ.get('DB_PORT', 5432)
DB_DATABASE = os.environ.get('DB_DATABASE', 'gitlabhq_production')
DB_URI = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{str(DB_PORT)}/{DB_DATABASE}'
DB_POOL_SIZE = 5
DB_POOL_TIMEOUT = 30
DB_POOL_RECYCLE = 600
DB_ENGINE_OPTIONS = {
    "pool_size": DB_POOL_SIZE,
    "pool_timeout": DB_POOL_TIMEOUT,
    "pool_recycle": DB_POOL_RECYCLE,
    "pool_pre_ping": True,
}

PROJECTS_CONFIG_PATH = os.environ.get("PROJECTS_CONFIG_PATH", "../config/projects.json")

def load_projects_config(config_path=PROJECTS_CONFIG_PATH):
    try:
        with open(config_path, 'r') as config_file:
            projects_config = json.load(config_file)
            return projects_config
    except FileNotFoundError:
        logging.warning(f"Configuration file {config_path} not found. Using default configuration.")
        return {
            "projects": []
        }

projects_config = load_projects_config()

PROJECTS = projects_config.get("projects", [])