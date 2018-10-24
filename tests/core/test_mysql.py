# -*- coding: utf-8 -*-

import pytest

from dbtrigger.core.mysql import MysqlRunner
from dbtrigger.models import Dialect


@pytest.fixture()
def expected_res():
    return [(1, 'foo'), (2, 'bar')]


@pytest.fixture(autouse=True)
def mysql_mock(monkeypatch, expected_res):

    class MysqlMock:

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
            yield from expected_res

    mock = MysqlMock()
    monkeypatch.setattr('pymysql.connect', lambda **_: mock)
    return mock


def test_mysql_runner(mysql_mock, query, expected_res):
    query.dialect = Dialect.mysql

    res = MysqlRunner(query).run()
    for row, expected in zip(res, expected_res):
        assert row == expected

    assert mysql_mock._cursor.query == query.query
    assert not mysql_mock._cursor.open
    assert not mysql_mock.connected
