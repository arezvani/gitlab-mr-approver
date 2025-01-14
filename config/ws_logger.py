import os
import sys
import logging
from flask import has_request_context, request

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_PATH not in sys.path:
    sys.path.insert(1, ROOT_PATH)

from config import conf

LOG_FORMAT = conf.LOG_FORMAT.get('webservice', '[%(asctime)s] [%(remote_addr)s] [%(user_agent)s] [%(caller_module)s] [%(method)s] [%(status_code)s] [%(path)s] [%(caller_class)s.%(caller_func)s] [%(levelname)s]: %(message)s')
LOG_LEVEL = conf.LOG_LEVEL.get('webservice', logging.INFO)


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.path = request.path
            record.method = request.method
            record.remote_addr = request.remote_addr
            record.user_agent = request.headers.get('User-Agent', 'N/A')
                            
        else:
            record.path = None
            record.method = None
            record.remote_addr = None
            record.user_agent = None

        record.caller_module = getattr(record, 'caller_module', record.module)
        record.caller_func = getattr(record, 'caller_func', record.funcName)
        record.caller_class = getattr(record, 'caller_class', 'N/A')
        record.status_code = getattr(record, 'status_code', 'N/A')

        return super().format(record)
    
formatter = RequestFormatter(LOG_FORMAT)