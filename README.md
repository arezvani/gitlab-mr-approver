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

configs:

| **Config**                | **Description**                                                                                  | **Default Value**                          | **Example**                             |
|---------------------------|--------------------------------------------------------------------------------------------------|--------------------------------------------|-----------------------------------------|
| `APP_SECRET_KEY`           | Secret key for the application, used for signing cookies or tokens.                             | `""`                                       | `D0ukrk87vh<]IgDYDowsyI]-jVLyX,&0`     |
| **Logging**                | Configuration for logging behavior.                                                              |                                            |                                         |
| `LOG_LEVEL.webservice`     | Log level for webservice logs.                                                                   | `logging.INFO`                            | `logging.DEBUG`                         |
| `LOG_LEVEL.base`           | Log level for base system logs.                                                                  | `logging.DEBUG`                           | `logging.WARNING`                       |
| `LOG_FORMAT.webservice`    | Log format for webservice logs.                                                                  | Custom log format                          | `"[%(asctime)s] [%(remote_addr)s] ..." ` |
| `LOG_FORMAT.base`          | Log format for base system logs.                                                                  | Custom log format                          | `"[%(asctime)s] [base] [%(levelname)s] ..." ` |
| `MASK_FIELDS`              | Fields to mask in logs (e.g., sensitive information).                                            | `['password']`                             | `['token', 'password']`                 |
| **GitLab Integration**     | Configuration for GitLab integration, including API tokens and URLs.                            |                                            |                                         |
| `GITLAB_URL`               | URL of your GitLab instance.                                                                     | `""`                                       | `https://gitlab.example.com`            |
| `GITLAB_TOKEN`             | GitLab API token used for authentication.                                                       | `""`                                       | `your_gitlab_token_here`                |
| `GITLAB_WEBHOOK_TOKEN`     | Token for verifying GitLab webhooks.                                                              | `""`                                       | `your_webhook_token_here`               |
| **Database Configuration** | Database connection details for PostgreSQL.                                                     |                                            |                                         |
| `DB_USERNAME`              | PostgreSQL database username.                                                                    | `postgres`                                 | `db_user`                               |
| `DB_PASSWORD`              | PostgreSQL database password.                                                                    | `""`                                       | `your_password_here`                    |
| `DB_HOST`                  | Host of the PostgreSQL database.                                                                 | `""`                                       | `localhost`                             |
| `DB_PORT`                  | Port of the PostgreSQL database.                                                                 | `5432`                                     | `5432`                                  |
| `DB_DATABASE`              | Name of the PostgreSQL database.                                                                 | `gitlabhq_production`                      | `my_gitlab_database`                    |
| `DB_URI`                   | Complete connection string for PostgreSQL database.                                              | Derived from above values                  | `postgresql://db_user:password@localhost:5432/gitlabhq_production` |
| `DB_POOL_SIZE`             | Number of database connections in the pool.                                                     | `5`                                        | `10`                                    |
| `DB_POOL_TIMEOUT`          | Timeout in seconds for acquiring a database connection.                                          | `30`                                       | `60`                                    |
| `DB_POOL_RECYCLE`          | Number of seconds before recycling a connection in the pool.                                     | `600`                                      | `300`                                   |
| `DB_ENGINE_OPTIONS`        | Additional database engine options.                                                              | Custom values (pooling, timeouts, etc.)     | `{"pool_size": 10, "pool_timeout": 60}`  |
| **Projects Configuration** | Path to the configuration file for project-specific settings.                                   | `../config/projects.json`                  | `config/projects.json`                  |
| `PROJECTS_CONFIG_PATH`     | Path to the JSON configuration file containing project-specific settings.                       | `../config/projects.json`                  | `config/projects.json`                  |

projects: An array of project-specific configurations:
- `project_id`: The ID of the GitLab project.
- `approvals`: A list of users required to approve the merge request.
- `min_approv`: The minimum number of approvals required to allow the merge request to proceed.
- `webhook_token`: The webhook token used in gitlab webhook calls.

> **Note:**
> You can set `GITLAB_WEBHOOK_TOKEN` as global and if you want set specific Gitlab webhook token, you can set that in `project.json` file.

## Usage

First you should run code by go to [src](./src) and run bellow command:

```bash
/usr/local/bin/gunicorn --workers 4 --bind <host>:<port> wsgi:app
```

### Docker

```bash
docker build -t <image_name>:<image_version> .  $(cat build.args | sed 's@^@--build-arg @g' | paste -s -d " ")
```

After setting up the application, configure your GitLab project to send webhook events to the Gitlab MR Approver server.

Example configuration:

- In your GitLab project, navigate to **Settings > Webhooks**.
- Add the URL where Gitlab MR Approver is hosted.
- Select the events you want to monitor, such as **Merge Request Events.**
- Save the webhook.

Gitlab MR Approver will now monitor merge requests and enforce your rules.

## PostgreSQL configuration

Gitlab MR Approver will call **Gitlab PostgreSQL server** to update merge request table. It will be a SELECT and an UPDATE query, like:

```sql
SELECT * FROM merge_requests WHERE iid = 1 AND target_project_id = 1;

UPDATE merge_requests SET merge_status = 'cannot_be_merged', merge_error = 'Requires at least 2 approvals from [user1 user2].' WHERE iid = 1 AND target_project_id = 1;
```

You can want to create a user for that. can be something like that:

```sql
CREATE USER webhook WITH PASSWORD '123456';
GRANT SELECT, UPDATE (merge_status,merge_error) ON TABLE merge_requests TO webhook;
```

# Demo
![1](./1.jpeg)

![2](./2.jpeg)

![3](./3.jpeg)
