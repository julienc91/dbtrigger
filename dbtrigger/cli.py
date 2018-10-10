# -*- coding: utf-8 -*-

from .config import settings
from .models import Server


class ServerCli:

    @classmethod
    def list(cls):
        keys = sorted(settings.servers.keys())
        for i, identifier in enumerate(keys, start=1):
            print("{}\t{}".format(i, identifier))

    @classmethod
    def add(cls, identifier: str, hostname: str, dialect: str, port: int=None):
        if identifier in settings.servers:
            raise ValueError('Another server already exists with this identifier')
        server = Server.from_config(identifier, hostname=hostname, dialect=dialect, port=port)
        settings.set_server(server)

        cls.list()

    @classmethod
    def delete(cls, identifier: str):
        if identifier not in settings.servers:
            raise ValueError('No server with this identifier')
        server = settings.servers[identifier]
        settings.del_server(server)

        cls.list()
