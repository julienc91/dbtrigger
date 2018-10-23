# -*- coding: utf-8 -*-

from ..models import Dialect


def run(query):
    dialect = query.database.server.dialect
    if dialect == Dialect.sqlite:
        from .sqlite import SqliteRunner
        runner = SqliteRunner
    elif dialect == Dialect.postgresql:
        from .postgresql import PostgresqlRunner
        runner = PostgresqlRunner
    else:
        raise NotImplementedError

    return runner(query).run()
