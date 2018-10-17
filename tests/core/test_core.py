# -*- coding: utf-8 -*-

import pytest

from dbtrigger.core import run
from dbtrigger.core.sqlite import SqliteRunner
from dbtrigger.models import Dialect


@pytest.mark.parametrize('dialect, expected', [
    (Dialect.sqlite, SqliteRunner),
])
def test_run(monkeypatch, query, dialect, expected):
    query.database.server.dialect = dialect

    monkeypatch.setattr(expected, 'run', lambda _: 'ok')
    res = run(query)
    assert res == 'ok'


def test_run_invalid_dialect(query):
    query.database.server.dialect = 'invalid dialect'
    with pytest.raises(NotImplementedError):
        run(query)
