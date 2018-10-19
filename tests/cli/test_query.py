# -*- coding: utf-8 -*-

import uuid

import pytest

from dbtrigger.cli import DatabaseCli, QueryCli, ServerCli
from dbtrigger.config import settings
from dbtrigger.models import Query


@pytest.fixture(autouse=True)
def add_database(server, database):
    ServerCli.add(server.identifier, server.hostname, server.dialect)
    DatabaseCli.add(database.identifier, server.identifier, database.name)


def test_list(query, database):
    QueryCli.add(query.identifier, database.identifier, query.query)
    QueryCli.list()


def test_list_no_queries():
    QueryCli.list()


def add_query(query, database):
    assert len(settings.queries) == 0
    QueryCli.add(query.identifier, database.identifier, query.query)
    assert len(settings.queries) == 1


def test_add_query_duplicate(query, database):
    QueryCli.add(query.identifier, database.identifier, query.query)
    with pytest.raises(ValueError):
        QueryCli.add(query.identifier, database.identifier, query.query)
    assert len(settings.queries) == 1


def test_add_query_not_existing_database(query):
    with pytest.raises(ValueError):
        QueryCli.add(query.identifier, str(uuid.uuid4()), query.query)
    assert len(settings.queries) == 0


def test_delete_query(query, database):
    QueryCli.add(query.identifier, database.identifier, query.query)
    QueryCli.delete(query.identifier)
    assert len(settings.queries) == 0


def test_delete_query_not_existing(query, database):
    QueryCli.add(query.identifier, database.identifier, query.query)
    QueryCli.delete(query.identifier)
    with pytest.raises(ValueError):
        QueryCli.delete(query.identifier)


def test_rename_query(query, database):
    QueryCli.add(query.identifier, database.identifier, query.query)
    new_identifier = str(uuid.uuid4())

    QueryCli.rename(query.identifier, new_identifier)
    assert len(settings.queries) == 1

    renamed_query = settings.queries[new_identifier]
    assert renamed_query.identifier == new_identifier
    assert renamed_query.query == query.query
    assert renamed_query.database.identifier == query.database.identifier


def test_rename_query_not_existing(query):
    new_identifier = str(uuid.uuid4())
    with pytest.raises(ValueError):
        QueryCli.rename(query.identifier, new_identifier)


def test_rename_query_duplicated(query, database):
    other_identifier = str(uuid.uuid4())
    other_query = Query(other_identifier, database, query.query)

    QueryCli.add(query.identifier, database.identifier, query.query)
    QueryCli.add(other_query.identifier, database.identifier, other_query.query)
    assert len(settings.queries) == 2

    with pytest.raises(ValueError):
        QueryCli.rename(query.identifier, other_identifier)


def test_run_query(monkeypatch, query, database):
    monkeypatch.setattr('dbtrigger.core.abstract.Runner.run', lambda _: [])
    QueryCli.add(query.identifier, database.identifier, query.query)
    QueryCli.run(query.identifier)


def test_run_query_not_existing(query):
    with pytest.raises(ValueError):
        QueryCli.run(query.identifier)
