# -*- coding: utf-8 -*-

import os
import sys
import json
import logging

from ..models import Database, Query, Server


class Settings:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, base_path):
        self.CONFIG_BASE_PATH = base_path
        self._config = {}
        self.load_config()

    def load_config(self):
        self._config = {}
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
            self._load_queries(config)
            self._config['triggers'] = config.get('triggers', {})
            self._config['reports'] = config.get('reports', {})
        except ValueError:
            logging.warning('Invalid config file')
            sys.exit(2)

    # --- servers ---
    def _load_servers(self, config):
        self._config['servers'] = {identifier: Server.from_config(identifier, **data)
                                   for identifier, data in config.get('servers', {}).items()}

    def set_server(self, server: Server):
        self._config['servers'][server.identifier] = server
        self.save()

    def del_server(self, server: Server):
        del self._config['servers'][server.identifier]
        self.save()

    # --- databases ---
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

    # --- queries ---
    def _load_queries(self, config):
        self._config['queries'] = {}
        for identifier, data in config.get('queries', {}).items():
            try:
                database = self._config['databases'][data['database']]
            except KeyError:
                logging.warning('Invalid config file')
                sys.exit(2)
            data['database'] = database
            self._config['queries'][identifier] = Query.from_config(identifier, **data)

    def set_query(self, query: Query):
        self._config['queries'][query.identifier] = query
        self.save()

    def del_query(self, query: Query):
        del self._config['queries'][query.identifier]
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
            'queries': {
                identifier: query.to_config()
                for identifier, query in self._config['queries'].items()
            },
            'triggers': self._config['triggers'],
            'reports': self._config['reports'],
        })
        with open(os.path.join(self.CONFIG_BASE_PATH, 'config.json'), 'w') as f:
            f.write(raw_config)

    @property
    def servers(self):
        return self._config['servers']

    @property
    def databases(self):
        return self._config['databases']

    @property
    def queries(self):
        return self._config['queries']
