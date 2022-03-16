# Microblog Server

This is a simple implementation of a microblog server.

> **WARNING:**
>
> It is **NOT** designed for production uses as there is no security consideration or implementation involved.

This code is released under BSD license.

## Requirements

| Software | Minimum Version | Tested Version | Note                    |
| --- | --- |----------------|-------------------------|
| Python | 3.7 | 3.9            | -                       |
| MySQL | 8 | 8              | Can use MariaDB instead |
| MariaDB | 10 | 10             | Can use MySQL instead |

## Install dependencies

Run `pip3 install -r requirements.txt`.

> It is highly recommended to run the code in **the virtual environment**.

## Database setup

| Property | Environment Variable | Required? | Default     |
|----------|----------------------|-----------|-------------|
| Hostname | `APP_DB_HOST`        | No        | `localhost` |
| Port     | `APP_DB_PORT`        | No        | `3306`      |
| DB name  | `APP_DB_NAME`        | No        | `microblog` |
| Username | `APP_DB_USERNAME`    | Yes       | -           |
| Password | `APP_DB_PASSWORD`    | Yes       | -           |


```sql
CREATE TABLE IF NOT EXISTS messages
(
    id VARCHAR(36) PRIMARY KEY,
    author_id VARCHAR(255),
    content TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
```

> This process can be simplified by just running `python3 -m microblog.setup --create-db`.
 
## How to run this app

```shell
FLASK_APP=microblog.web FLASK_ENV=development flask run
```