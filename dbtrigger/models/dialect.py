# -*- coding: utf-8 -*-

from enum import Enum

from ..exceptions import UnavailableDialect


unavailable_dialects = {}


class Dialect(Enum):
    sqlite = "sqlite"
    mysql = "mysql"
    postgresql = "postgresql"

    def assert_available(self):
        error_message = unavailable_dialects.get(self)
        if error_message:
            raise UnavailableDialect(error_message)


try:
    import pymysql  # noqa F401
except ImportError:
    unavailable_dialects[Dialect.mysql] = "Please install PyMySQL to enable MySQL dialect"

try:
    import psycopg2  # noqa F401
except ImportError:
    unavailable_dialects[Dialect.postgresql] = "Please install psycopg2 to enable PostgreSQL dialect"
