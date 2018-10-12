# -*- coding: utf-8 -*-

import os
import sys
import json
import logging

import appdirs

from .models import Server, Database


class Settings:

    CONFIG_BASE_PATH = appdirs.user_data_dir('dbtrigger')

    def __init__(self):
        self._config = {}
        self.load_config()

    def load_config(self):
        try:
            with open(os.path.join(self.CONFIG_BASE_PATH, 'config.json'), 'rb') as f:
                config = f.read()
        except IOError:
            os.makedirs(self.CONFIG_BASE_PATH, exist_ok=True)
            config = "{}"

        try:
            config = json.loads(config)
            self._load_servers(config)
            self._load_databases(config)
            self._config['triggers'] = config.get('triggers', {})
            self._config['reports'] = config.get('reports', {})
            self._config['queries'] = config.get('queries', {})
        except ValueError:
            logging.warning('Invalid config file')
            sys.exit(2)

    def _load_servers(self, config):
        self._config['servers'] = {identifier: Server.from_config(identifier, **data)
                                   for identifier, data in config.get('servers', {}).items()}

    def set_server(self, server: Server):
        self._config['servers'][server.identifier] = server
        self.save()

    def del_server(self, server: Server):
        del self._config['servers'][server.identifier]
        self.save()

    def _load_databases(self, config):
        self._config['databases'] = {}
        for identifier, data in config.get('databases', {}).items():
            try:
                server = self._config['servers'][data['server']]
            except KeyError:
                logging.warning('Invalid config file')
                sys.exit(2)
            data['server'] = server
            self._config['databases'][identifier] = Database.from_config(identifier, **data)

    def set_database(self, database: Database):
        self._config['databases'][database.identifier] = database
        self.save()

    def del_database(self, database: Database):
        del self._config['databases'][database.identifier]
        self.save()

    def save(self):
        os.makedirs(self.CONFIG_BASE_PATH, exist_ok=True)
        raw_config = json.dumps({
            'servers': {
                identifier: server.to_config()
                for identifier, server in self._config['servers'].items()
            },
            'databases': {
                identifier: database.to_config()
                for identifier, database in self._config['databases'].items()
            },
            'triggers': self._config['triggers'],
            'reports': self._config['reports'],
            'queries': self._config['queries'],
        })
        with open(os.path.join(self.CONFIG_BASE_PATH, 'config.json'), 'w') as f:
            f.write(raw_config)

    @property
    def servers(self):
        return self._config['servers']

    @property
    def databases(self):
        return self._config['databases']


settings = Settings()
