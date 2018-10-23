# -*- coding: utf-8 -*-

import pytest

from dbtrigger.core.postgresql import PostgresqlRunner
from dbtrigger.models import Dialect


@pytest.fixture(autouse=True)
def postgresql_mock(monkeypatch):

    class PostgresqlMock:
        res = [(1, 'foo'), (2, 'bar')]

        def __init__(self):
            self.connected = True
            self._cursor = None

        def close(self):
            self.connected = False

        def cursor(self):
            assert self.connected
            self._cursor = CursorMock()
            return self._cursor

    class CursorMock:
        res = [(1, 'foo'), (2, 'bar')]

        def __init__(self):
            self.open = False
            self.query = None

        def __enter__(self):
            self.open = True
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.open = False

        def execute(self, query):
            assert self.open
            self.query = query

        def fetchall(self):
            assert self.open
            assert self.query
            yield from self.res

    mock = PostgresqlMock()
    monkeypatch.setattr('psycopg2.connect', lambda **_: mock)
    return mock


def test_postgresql_runner(postgresql_mock, query):
    query.dialect = Dialect.postgresql

    res = PostgresqlRunner(query).run()
    for row, expected in zip(res, postgresql_mock.res):
        assert row == expected

    assert postgresql_mock._cursor.query == query.query
    assert not postgresql_mock._cursor.open
    assert not postgresql_mock.connected
