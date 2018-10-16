# -*- coding: utf-8 -*-

from .database import Database


class Query:

    def __init__(
        self,
        identifier: str,
        database: Database,
        query: str,
    ):
        self.identifier = identifier
        self.database = database
        self.query = query

    def __str__(self):
        return self.identifier

    def __repr__(self):
        return self.identifier

    @classmethod
    def from_config(cls, identifier, **config):
        return cls(identifier=identifier, **config)

    def to_config(self):
        return {
            'database': self.database.identifier,
            'query': self.query,
        }

    def run(self):
        raise NotImplementedError
