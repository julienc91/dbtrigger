# -*- coding: utf-8 -*-

from typing import Optional

from ..config import settings
from ..models import Server
from .database import DatabaseCli


class ServerCli:
    """
    Command-line interface to manage servers.
    """

    @classmethod
    def list(cls) -> None:
        """
        Print all the registered servers.
        """
        keys = sorted(settings.servers.keys())
        for i, identifier in enumerate(keys, start=1):
            print("{}\t{}".format(i, identifier))

    @classmethod
    def add(cls, identifier: str, hostname: str, dialect: str, port: Optional[int]=None) -> None:
        """
        Create a new server
        :param identifier: a unique identifier for the server to create
        :param hostname: hostname of the server to create
        :param dialect: the dialect on this server
        :param port: the port to use to connect to the server. Default port depends on the selected dialect.
        """
        if identifier in settings.servers:
            raise ValueError('Another server already exists with this identifier')
        server = Server.from_config(identifier, hostname=hostname, dialect=dialect, port=port)
        settings.set_server(server)

    @classmethod
    def delete(cls, identifier: str) -> None:
        """
        Delete a server from the current list of servers
        :param identifier: the identifier associated to the server to delete
        """
        if identifier not in settings.servers:
            raise ValueError('No server with this identifier')
        server = settings.servers[identifier]

        # delete linked databases
        databases_to_delete = [database for database in settings.databases.values()
                               if database.server.identifier == server.identifier]
        for database in databases_to_delete:
            DatabaseCli.delete(database.identifier)

        settings.del_server(server)

    @classmethod
    def update(cls, identifier: str, hostname: Optional[str]=None,
               dialect: Optional[str]=None, port: Optional[int]=None) -> None:
        """
        Update an existing server. Only set fields you want to change.
        :param identifier: the identifier associated to the server to update
        :param hostname: the new hostname to use for this server
        :param dialect: the new dialect to use for this server
        :param port: the new port to use for this server
        """
        if identifier not in settings.servers:
            raise ValueError('No server with this identifier')

        server = settings.servers[identifier]
        kwargs = {
            'hostname': hostname or server.hostname,
            'dialect': dialect or server.dialect,
            'port': port or server.port
        }
        updated_server = Server.from_config(identifier, **kwargs)
        settings.set_server(updated_server)

    @classmethod
    def rename(cls, identifier: str, new_identifier: str) -> None:
        """
        Update the identifier of an already created server.
        :param identifier: the current identifier associated to the server to update
        :param new_identifier: the new identifier to use instead
        """
        if identifier not in settings.servers:
            raise ValueError('No server with this identifier')
        if new_identifier in settings.servers:
            raise ValueError('Another server already exists with this identifier')

        server = settings.servers[identifier]
        kwargs = {
            'hostname': server.hostname,
            'dialect': server.dialect,
            'port': server.port
        }
        updated_server = Server.from_config(new_identifier, **kwargs)
        settings.set_server(updated_server)

        # update linked databases
        databases_to_update = [database for _, database in settings.databases.items()
                               if database.server.identifier == server.identifier]
        for database in databases_to_update:
            DatabaseCli.update(database.identifier, server=updated_server.identifier)

        # delete old server
        settings.del_server(server)
