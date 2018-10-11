# -*- coding: utf-8 -*-

from typing import Optional, Union

from .dialect import Dialect
from ..exceptions import ConfigError


class Server:

    def __init__(
        self,
        identifier: str,
        hostname: str,
        dialect: Union[Dialect, str],
        port: Optional[int]=None,
    ):
        if not hostname:
            raise ConfigError('Missing hostname parameter')

        self.identifier = identifier
        self.hostname = hostname
        self.dialect = dialect
        self.port = port
        self._parse_dialect()

    def __str__(self):
        return self.identifier

    def __repr__(self):
        return self.identifier

    def _parse_dialect(self):
        try:
            self.dialect = Dialect(self.dialect)
        except ValueError as exc:
            raise ConfigError('Invalid dialect') from exc
        self.dialect.assert_available()
        {
            Dialect.sqlite: self.__load_sqlite,
            Dialect.mysql: self.__load_mysql,
            Dialect.postgresql: self.__load_postgresql,
        }[self.dialect]()

    def __load_sqlite(self):
        if self.port is not None:
            raise ConfigError('Port should not be set with sqlite dialect')

    def __load_mysql(self):
        if self.port is None:
            self.port = 3306

    def __load_postgresql(self):
        if self.port is None:
            self.port = 5432

    @classmethod
    def from_config(cls, identifier, **config):
        return cls(identifier=identifier, **config)

    def to_config(self):
        return {
            'hostname': self.hostname,
            'port': self.port,
            'dialect': self.dialect.name,
        }
