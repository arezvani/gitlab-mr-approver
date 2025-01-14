import os
import sys
import logging
import logging.config

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_PATH not in sys.path:
    sys.path.insert(1, ROOT_PATH)

from config import conf

log_format = conf.LOG_FORMAT.get('base', '[%(asctime)s] [base] [%(levelname)s]: %(message)s')
log_level = conf.LOG_LEVEL.get('base', logging.INFO)

logger = logging.getLogger('base')
logger.setLevel(level=log_level)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter(log_format))
logger.addHandler(handler)