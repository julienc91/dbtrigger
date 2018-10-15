# -*- coding: utf-8 -*-

from typing import Optional

from ..config import settings
from ..models import Database


class DatabaseCli:
    """
    Command-line interface to manage databases.
    """

    @classmethod
    def list(cls) -> None:
        """
        Print all the registered databases.
        """
        keys = sorted(settings.databases.keys())
        for i, identifier in enumerate(keys, start=1):
            print("{}\t{}".format(i, identifier))

    @classmethod
    def add(cls, identifier: str, server: str, name: str,
            username: Optional[str]=None, password: Optional[str]=None) -> None:
        """
        Create a new database.
        :param identifier: a unique identifier for the database to create
        :param server: identifier of the server to link the database to
        :param name: name of the database
        :param username: the username to use to connect to this database
        :param password: the password to use to connect to this database
        """
        if identifier in settings.databases:
            raise ValueError('Another database already exists with this identifier')
        if server not in settings.servers:
            raise ValueError('No server with this identifier')
        server = settings.servers[server]
        database = Database.from_config(identifier, server=server, name=name, username=username, password=password)
        settings.set_database(database)

    @classmethod
    def delete(cls, identifier: str) -> None:
        """
        Delete a database from the current list of databases.
        :param identifier: the identifier associated to the database to delete
        """
        if identifier not in settings.databases:
            raise ValueError('No database with this identifier')
        database = settings.databases[identifier]
        settings.del_database(database)

    @classmethod
    def update(cls, identifier: str, server: Optional[str]=None, name: Optional[str]=None,
               username: Optional[str]=None, password: Optional[str]=None) -> None:
        """
        Update an existing database. Only set fields you want to change.
        :param identifier: the identifier associated to the database to update
        :param server: the new server to link to this database
        :param name: the new name of this database
        :param username: the new username to use for this database
        :param password: the new password to use for this database
        """
        if identifier not in settings.databases:
            raise ValueError('No database with this identifier')
        if server and server not in settings.servers:
            raise ValueError('No server with this identifier')

        if server:
            server = settings.servers[server]
        database = settings.databases[identifier]
        kwargs = {
            'server': server or database.server,
            'name': name or database.name,
            'username': username or database.username,
            'password': password or database.password
        }
        updated_database = Database.from_config(identifier, **kwargs)
        settings.set_database(updated_database)

    @classmethod
    def rename(cls, identifier: str, new_identifier: str) -> None:
        """
        Update the identifier of an already created database.
        :param identifier: the current identifier associated to the database to update
        :param new_identifier: the new identifier to use instead
        """
        if identifier not in settings.databases:
            raise ValueError('No server with this identifier')
        if new_identifier in settings.databases:
            raise ValueError('Another database already exists with this identifier')

        database = settings.databases[identifier]
        kwargs = {
            'server': database.server,
            'name': database.name,
            'username': database.username,
            'password': database.password
        }
        updated_database = Database.from_config(new_identifier, **kwargs)
        settings.set_database(updated_database)
        settings.del_database(database)
