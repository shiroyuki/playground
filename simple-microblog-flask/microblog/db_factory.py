from typing import Optional

from sqlalchemy import create_engine

from microblog.helper import env


class DbFactory:
    @staticmethod
    def engine(url: str, echo=False):
        actual_url = url
        return create_engine(actual_url, echo=echo, future=True)

    @staticmethod
    def get_url():
        username = env('APP_DB_USERNAME')
        password = env('APP_DB_PASSWORD')
        db_host = env('APP_DB_HOST', required=False, default='localhost')
        db_port = env('APP_DB_PORT', required=False, default='3306')
        db_name = env('APP_DB_NAME', required=False, default='microblog')
        return f'mysql+pymysql://{username}:{password}@{db_host}:{db_port}/{db_name}'
