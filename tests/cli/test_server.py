# -*- coding: utf-8 -*-

from dbtrigger.cli.server import ServerCli
from dbtrigger.config import settings
from dbtrigger.models import Dialect


def test_add_server():
    assert len(settings.servers) == 0

    identifier = 'server1'
    hostname = 'example.com'
    dialect = Dialect.sqlite

    ServerCli.add(identifier, hostname, dialect.name)
    assert len(settings.servers) == 1

    server = settings.servers[identifier]
    assert server.identifier == identifier
    assert server.hostname == hostname
    assert server.dialect == dialect
