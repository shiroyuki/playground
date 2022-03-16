import re
from argparse import ArgumentParser
from urllib.parse import urlparse

from sqlalchemy import text

from microblog.db_factory import DbFactory


def set_up_database(create_db: bool):
    url = DbFactory.get_url()
    db_name = urlparse(url).path[1:]

    with DbFactory.engine(re.sub(r'/[^/]+$', '', url)).connect() as conn:
        # language=sql
        conn.execute(text(f'CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'))

    with DbFactory.engine(url).connect() as conn:

        conn.execute(text(
            # language=sql
            """
                CREATE TABLE IF NOT EXISTS messages
                (
                    id VARCHAR(36) PRIMARY KEY,
                    author_id VARCHAR(255),
                    content TEXT,
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP
                )
                CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
            """
        ))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--create-db', action='store_true', required=False)

    args = parser.parse_args()

    set_up_database(args.create_db)
