# -*- coding: utf-8 -*-

from ..models import Dialect


def run(query):
    dialect = query.database.server.dialect
    if dialect == Dialect.sqlite:
        from .sqlite import SqliteRunner
        runner = SqliteRunner
    else:
        raise NotImplementedError

    return runner(query).run()
