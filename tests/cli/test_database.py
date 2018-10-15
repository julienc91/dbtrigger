# -*- coding: utf-8 -*-

import uuid

import pytest

from dbtrigger.cli.server import DatabaseCli, ServerCli
from dbtrigger.config import settings
from dbtrigger.models import Database, Dialect, Server


@pytest.fixture(autouse=True)
def add_server(server):
    ServerCli.add(server.identifier, server.hostname, server.dialect)


def compare_databases(db1, db2):
    assert db1.identifier == db2.identifier
    assert db1.server.identifier == db2.server.identifier
    assert db1.name == db2.name
    assert db1.username == db2.username
    assert db1.password == db2.password
    return True


def test_list(database, server):
    DatabaseCli.add(database.identifier, server.identifier, database.name, database.username, database.password)
    DatabaseCli.list()


def test_list_no_databasess():
    DatabaseCli.list()


def add_database(database, server):
    assert len(settings.databases) == 0
    DatabaseCli.add(database.identifier, server.identifier, database.name, database.username, database.password)
    assert len(settings.databases) == 1
    assert compare_databases(database, settings.databases[database.identifier])


def test_add_database_duplicate(database, server):
    DatabaseCli.add(database.identifier, server.identifier, database.name, database.username, database.password)
    with pytest.raises(ValueError):
        DatabaseCli.add(database.identifier, server.identifier, database.name, database.username, database.password)
    assert len(settings.databases) == 1


def test_add_database_not_existing_server(database):
    with pytest.raises(ValueError):
        DatabaseCli.add(database.identifier, str(uuid.uuid4()), database.name, database.username, database.password)
    assert len(settings.databases) == 0


def test_delete_database(database, server):
    DatabaseCli.add(database.identifier, server.identifier, database.name, database.username, database.password)
    DatabaseCli.delete(database.identifier)
    assert len(settings.databases) == 0


def test_delete_database_not_existing(database, server):
    DatabaseCli.add(database.identifier, server.identifier, database.name, database.username, database.password)
    DatabaseCli.delete(database.identifier)
    with pytest.raises(ValueError):
        DatabaseCli.delete(database.identifier)


def test_update_database_not_existing(database, server):
    with pytest.raises(ValueError):
        DatabaseCli.update(database.identifier, server, 'new name', 'new username', 'new password')


def test_update_database_not_existing_server(database, server):
    DatabaseCli.add(database.identifier, server.identifier, database.name, database.username, database.password)
    with pytest.raises(ValueError):
        DatabaseCli.update(database.identifier, str(uuid.uuid4()), 'new name', 'new username', 'new password')


def test_rename_database(database, server):
    DatabaseCli.add(database.identifier, server.identifier, database.name, database.username, database.password)
    new_identifier = str(uuid.uuid4())

    DatabaseCli.rename(database.identifier, new_identifier)
    assert len(settings.databases) == 1

    renamed_db = settings.databases[new_identifier]
    database.identifier = new_identifier
    assert compare_databases(database, renamed_db)


def test_rename_database_not_existing(database):
    new_identifier = str(uuid.uuid4())
    with pytest.raises(ValueError):
        DatabaseCli.rename(database.identifier, new_identifier)


def test_rename_database_duplicated(database, server):
    other_identifier = str(uuid.uuid4())
    other_db = Database(other_identifier, server, database.name, database.username, database.password)

    DatabaseCli.add(database.identifier, server.identifier, database.name, database.username, database.password)
    DatabaseCli.add(other_db.identifier, server.identifier, other_db.name, other_db.username, other_db.password)
    assert len(settings.databases) == 2

    with pytest.raises(ValueError):
        DatabaseCli.rename(database.identifier, other_identifier)

    assert compare_databases(database, settings.databases[database.identifier])
    assert compare_databases(other_db, settings.databases[other_identifier])
