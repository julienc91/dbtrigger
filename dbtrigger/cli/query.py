# -*- coding: utf-8 -*-

from ..config import settings
from ..core import run
from ..models import Query


class QueryCli:
    """
    Command-line interface to manage queries.
    """

    @classmethod
    def list(cls) -> None:
        """
        Print all the registered databases.
        """
        keys = sorted(settings.queries.keys())
        for i, identifier in enumerate(keys, start=1):
            print("{}\t{}".format(i, settings.queries[identifier]))

    @classmethod
    def add(cls, identifier: str, database: str, query: str) -> None:
        """
        Create a new query.
        :param identifier: a unique identifier for the query to create
        :param database: identifier of the database to link the query to
        :param query: the raw SQL query
        """
        if identifier in settings.queries:
            raise ValueError('Another query already exists with this identifier')
        if database not in settings.databases:
            raise ValueError('No database with this identifier')
        database = settings.databases[database]
        query = Query.from_config(identifier, database=database, query=query)
        settings.set_query(query)

    @classmethod
    def delete(cls, identifier: str) -> None:
        """
        Delete a query from the current list of queries.
        :param identifier: the identifier associated to the database to delete
        """
        if identifier not in settings.queries:
            raise ValueError('No query with this identifier')
        query = settings.queries[identifier]
        settings.del_query(query)

    @classmethod
    def rename(cls, identifier: str, new_identifier: str) -> None:
        """
        Update the identifier of an already created query.
        :param identifier: the current identifier associated to the query to update
        :param new_identifier: the new identifier to use instead
        """
        if identifier not in settings.queries:
            raise ValueError('No query with this identifier')
        if new_identifier in settings.queries:
            raise ValueError('Another query already exists with this identifier')

        query = settings.queries[identifier]
        kwargs = {
            'database': query.database,
            'query': query.query,
        }
        updated_query = Query.from_config(new_identifier, **kwargs)
        settings.set_query(updated_query)
        settings.del_query(query)

    @classmethod
    def run(cls, identifier: str) -> None:
        """
        Run a query.
        :param identifier: the identifier for the query to run
        """
        if identifier not in settings.queries:
            raise ValueError('No query with this identifier')

        query = settings.queries[identifier]
        res = run(query)
        for row in res:
            print(row)
