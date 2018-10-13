# -*- coding: utf-8 -*-

from typing import Optional

from .server import Server


class Database:

    def __init__(
        self,
        identifier: str,
        server: Server,
        name: str,
        username: Optional[str]=None,
        password: Optional[str]=None,
    ):
        self.identifier = identifier
        self.server = server
        self.name = name
        self.username = username
        self.password = password

    def __str__(self):
        return self.identifier

    def __repr__(self):
        return self.identifier

    @classmethod
    def from_config(cls, identifier, **config):
        return cls(identifier=identifier, **config)

    def to_config(self):
        return {
            'server': self.server.identifier,
            'name': self.name,
            'username': self.username,
            'password': self.password,
        }
