import os
import sys
import json
import logging
from flask_cors import CORS
from flask import Flask, request, jsonify

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_PATH not in sys.path:
    sys.path.insert(1, ROOT_PATH)

from extensions import db
from app_config import AppConfig
from utils.gitlab_functions import *
from config.ws_logger import formatter, LOG_LEVEL

app = Flask(__name__)
app.config.from_object(AppConfig)

CORS(app)

db.init_app(app)

app.logger.setLevel(LOG_LEVEL)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(formatter)
app.logger.handlers.clear()
app.logger.addHandler(handler)


@app.route('/state', methods=['GET', 'OPTIONS'])
def state():
    if request.method == 'OPTIONS':
        return '', 200
    return jsonify({"status": "Service is ready"}), 200

@app.route('/api/v1/approve', methods=['POST', 'OPTIONS'])
def approve():
    if request.method == 'OPTIONS':
        return '', 200

    try:
        request_token = request.headers.get("X-Gitlab-Token")
        
        callback = request.json
        if not callback:
            return jsonify({"error": "Invalid payload"}), 400

        app.logger.info("Received webhook: %s", json.dumps(callback))

        cb_action = callback.get('object_attributes', {}).get('action')
        cb_mr_id = callback.get('object_attributes', {}).get('iid')
        cb_project = callback.get('object_attributes', {}).get('target_project_id')

        project_config = next((p for p in projects_config if p["project_id"] == cb_project), None)
        
        project_webhook_token = project_config.get("webhook_token") if project_config else gitlab_webhook_token
        if project_webhook_token and request_token != project_webhook_token:
            app.logger.warning("Invalid webhook token provided.")
            return jsonify({"error": "Unauthorized"}), 401

        if cb_action in ["open", "reopen", "approved", "unapproved"]:
            reinforce_mr_rule(project_config, cb_mr_id)

        return jsonify({"msg": "Merge event received"}), 200

    except Exception as e:
        app.logger.error("Error processing webhook: %s", e)
        return jsonify({"error": str(e)}), 500
