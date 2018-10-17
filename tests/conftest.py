# -*- coding: utf-8 -*-

import uuid

import pytest

import dbtrigger.config
from dbtrigger.models import Database, Dialect, Query, Server


@pytest.fixture(scope="function", autouse=True)
def settings(monkeypatch, tmpdir):
    monkeypatch.setattr(dbtrigger.config.settings, 'CONFIG_BASE_PATH', tmpdir.strpath)
    dbtrigger.config.settings.load_config()
    yield
    dbtrigger.config.settings.load_config()


@pytest.fixture()
def server():
    return Server(str(uuid.uuid4()), 'example.com', Dialect.sqlite)


@pytest.fixture()
def database(server):
    return Database(str(uuid.uuid4()), server, 'db', 'foo', 'password')


@pytest.fixture()
def query(database):
    return Query(str(uuid.uuid4()), database, "SELECT * FROM foo;")
