# -*- coding: utf-8 -*-

import pytest

from dbtrigger.core.sqlite import SqliteRunner
from dbtrigger.models import Dialect


@pytest.fixture(autouse=True)
def sqlite_mock(monkeypatch):

    class SqliteMock:
        res = [(1, 'foo'), (2, 'bar')]

        def __init__(self):
            self.connected = True
            self.query = None

        def close(self):
            self.connected = False

        def execute(self, query):
            assert self.connected
            self.query = query
            yield from self.res

    mock = SqliteMock()
    monkeypatch.setattr('sqlite3.connect', lambda _: mock)
    return mock


def test_sqlite_runner(sqlite_mock, query):
    query.dialect = Dialect.sqlite

    res = SqliteRunner(query).run()
    for row, expected in zip(res, sqlite_mock.res):
        assert row == expected

    assert sqlite_mock.query == query.query
    assert not sqlite_mock.connected
