# -*- coding: utf-8 -*-

import uuid

import pytest
from unittest.mock import MagicMock

from dbtrigger.cli import DatabaseCli, ServerCli
from dbtrigger.config import settings
from dbtrigger.models import Dialect, Server


def compare_servers(server1, server2):
    assert server1.identifier == server2.identifier
    assert server1.hostname == server2.hostname
    assert server1.dialect == server2.dialect
    return True


def test_list(server):
    ServerCli.add(server.identifier, server.hostname, server.dialect.name)
    ServerCli.list()


def test_list_no_servers():
    ServerCli.list()


def test_add_server(server):
    assert len(settings.servers) == 0
    ServerCli.add(server.identifier, server.hostname, server.dialect.name)
    assert len(settings.servers) == 1
    assert compare_servers(server, settings.servers[server.identifier])


def test_add_server_duplicate(server):
    ServerCli.add(server.identifier, server.hostname, server.dialect.name)
    with pytest.raises(ValueError):
        ServerCli.add(server.identifier, server.hostname, server.dialect.name)
    assert len(settings.servers) == 1


def test_add_server_unavailable_dialect(monkeypatch, server):
    monkeypatch.setattr('dbtrigger.models.dialect.Dialect.mysql.assert_available', MagicMock(side_effect=ValueError))
    with pytest.raises(ValueError):
        ServerCli.add(server.identifier, server.hostname, Dialect.mysql.name)


def test_delete_server(server):
    ServerCli.add(server.identifier, server.hostname, server.dialect.name)
    ServerCli.delete(server.identifier)
    assert len(settings.servers) == 0


def test_delete_server_with_database(server, database):
    ServerCli.add(server.identifier, server.hostname, server.dialect.name)
    DatabaseCli.add(database.identifier, server.identifier, database.name, database.username, database.password)
    assert len(settings.servers) == 1
    assert len(settings.databases) == 1

    ServerCli.delete(server.identifier)
    assert len(settings.servers) == 0
    assert len(settings.databases) == 0


def test_delete_server_not_existing(server):
    ServerCli.add(server.identifier, server.hostname, server.dialect.name)
    ServerCli.delete(server.identifier)
    with pytest.raises(ValueError):
        ServerCli.delete(server.identifier)


def test_update_server(server):
    ServerCli.add(server.identifier, server.hostname, server.dialect.name)
    updated_server = Server(server.identifier, 'example.org', Dialect.postgresql)

    ServerCli.update(server.identifier, updated_server.hostname, updated_server.dialect.name)
    assert len(settings.servers) == 1
    assert compare_servers(updated_server, settings.servers[server.identifier])


def test_update_server_not_existing(server):
    with pytest.raises(ValueError):
        ServerCli.update(server.identifier, 'new hostname', Dialect.mysql.name)


def test_update_serer_unavailable_dialect(monkeypatch, server):
    ServerCli.add(server.identifier, server.hostname, server.dialect.name)
    monkeypatch.setattr('dbtrigger.models.dialect.Dialect.mysql.assert_available', MagicMock(side_effect=ValueError))
    with pytest.raises(ValueError):
        ServerCli.update(server.identifier, server.hostname, Dialect.mysql.name)



def test_rename_server(server):
    ServerCli.add(server.identifier, server.hostname, server.dialect.name)
    new_identifier = str(uuid.uuid4())

    ServerCli.rename(server.identifier, new_identifier)
    assert len(settings.servers) == 1

    renamed_server = settings.servers[new_identifier]
    server.identifier = new_identifier
    assert compare_servers(server, renamed_server)


def test_rename_server_with_database(server, database):
    ServerCli.add(server.identifier, server.hostname, server.dialect.name)
    DatabaseCli.add(database.identifier, server.identifier, database.name, database.username, database.password)

    new_identifier = str(uuid.uuid4())
    ServerCli.rename(server.identifier, new_identifier)
    assert len(settings.servers) == 1
    assert len(settings.databases) == 1

    assert settings.databases[database.identifier].server.identifier == new_identifier


def test_rename_server_not_existing(server):
    new_identifier = str(uuid.uuid4())
    with pytest.raises(ValueError):
        ServerCli.rename(server.identifier, new_identifier)


def test_rename_server_duplicated(server):
    other_identifier = str(uuid.uuid4())
    other_server = Server(other_identifier, server.hostname, server.dialect)

    ServerCli.add(server.identifier, server.hostname, server.dialect.name)
    ServerCli.add(other_server.identifier, other_server.hostname, other_server.dialect.name)
    assert len(settings.servers) == 2

    with pytest.raises(ValueError):
        ServerCli.rename(server.identifier, other_identifier)

    assert compare_servers(server, settings.servers[server.identifier])
    assert compare_servers(other_server, settings.servers[other_identifier])
