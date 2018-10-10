# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class Server:

    identifier: str

    hostname: str
    port: int
    dialect: str

    def __str__(self):
        return self.identifier

    def __repr__(self):
        return self.identifier

    @classmethod
    def from_config(cls, identifier, **config):
        return cls(identifier=identifier, **config)

    def to_config(self):
        return {
            'hostname': self.hostname,
            'port': self.port,
            'dialect': self.dialect
        }
