import os
import sys
import requests
from extensions import db
from sqlalchemy import text

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_PATH not in sys.path:
    sys.path.insert(1, ROOT_PATH)

from config import conf
from config.base_logger import logger

# Global configuration
gitlab_url = conf.GITLAB_URL
gitlab_token = conf.GITLAB_TOKEN
gitlab_webhook_token = conf.GITLAB_WEBHOOK_TOKEN or None
projects_config = conf.PROJECTS or []


def reinforce_mr_rule(project_config, mr_id):
    project_id = project_config["project_id"]
    logger.info("Reinforcing MR rule for Project: %d, MR: %d", project_id, mr_id)

    try:
        url = f"{gitlab_url}/api/v4/projects/{project_id}/merge_requests/{mr_id}/approvals"
        headers = {
            "PRIVATE-TOKEN": gitlab_token,
            "Accept": "application/json"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        approvals = response.json()
        pending_approvals = calculate_pending_approvals(approvals, project_config)

        if pending_approvals == 0:
            update_merge_status(project_id, mr_id, "can_be_merged", "")
        else:
            msg = f"Requires at least {pending_approvals} more approvals"
            update_merge_status(project_id, mr_id, "cannot_be_merged", msg)

    except Exception as e:
        logger.error("Error reinforcing MR rule: %s", e)

def calculate_pending_approvals(approvals, project_config):
    required_approvals = project_config.get("min_approv", 1)
    approved_users = [by["user"]["username"] for by in approvals.get("approved_by", [])]
    expected_approvers = project_config.get("approvals", [])
    valid_approvals = [user for user in approved_users if user in expected_approvers]
    return max(0, required_approvals - len(valid_approvals))

def update_merge_status(project_id, mr_id, status, error_message):
    try:
        query = text("""
            UPDATE merge_requests
            SET merge_status = :status,
                merge_error = :error_message
            WHERE target_project_id = :project_id AND iid = :mr_id
        """)
        db.session.execute(query, {
            "status": status,
            "error_message": error_message,
            "project_id": project_id,
            "mr_id": mr_id
        })
        db.session.commit()
        logger.info("Merge status updated: Project %d, MR %d", project_id, mr_id)
    except Exception as e:
        logger.error("Error updating merge status: %s", e)