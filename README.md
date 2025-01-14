# Gitlab MR Approver
Gitlab MR Approver is a service that integrates with GitLab to enforce approval workflows for merge requests. It listens to GitLab webhook events, processes approval requirements, and updates the merge status accordingly. The system checks if the minimum number of approvals are met for a merge request to be merged and can be customized to suit project-specific requirements.

## Features
- Automatically enforces minimum approval rules for GitLab merge requests.
- Supports project-specific approval requirements.
- Webhook integration for handling GitLab events.
- Updates merge status based on approval requirements.
- Customizable logging and configuration.

# Configuration

Gitlab MR Approver uses a JSON configuration file to manage its settings. Below is an example of the required structure:

```json
{
  "projects": [
    {
      "project_id": <ID>,
      "approvals": ["<user1>", "<user2>", "<user3>"],
      "webhook_token": "<webhook token>",
      "min_approv": 2
    }
  ]
}
```

### Configuration Fields

projects: An array of project-specific configurations:
- project_id: The ID of the GitLab project.
- approvals: A list of users required to approve the merge request.
- min_approv: The minimum number of approvals required to allow the merge request to proceed.
- webhook_token: The webhook token used in gitlab webhook calls.

## Usage

After setting up the application, configure your GitLab project to send webhook events to the Gitlab MR Approver server.

Example configuration:

- In your GitLab project, navigate to **Settings > Webhooks"".
- Add the URL where Gitlab MR Approver is hosted.
- Select the events you want to monitor, such as "Merge Request Events."
- Save the webhook.

Gitlab MR Approver will now monitor merge requests and enforce your rules.

## PostgreSQL configuration

Gitlab MR Approver will call gitlab postgreSQL server to update merge request table. It will be a SELECT and an UPDATE query, like:

```sql
SELECT * FROM merge_requests WHERE iid = 1 AND target_project_id = 1;

UPDATE merge_requests SET merge_status = 'cannot_be_merged', merge_error = 'Requires at least 2 approvals from [user1 user2].' WHERE iid = 1 AND target_project_id = 1;
```

You can want to create a user for that. can be something like that:

```sql
CREATE USER webhook WITH PASSWORD '123456';
GRANT SELECT, UPDATE (merge_status,merge_error) ON TABLE merge_requests TO webhook;
```
