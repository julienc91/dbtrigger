# -*- coding: utf-8 -*-

import os
import sqlite3

from .abstract import Runner
from ..models import Query


class SqliteRunner(Runner):

    def __init__(self, query: Query):
        super().__init__(query)
        self._conn = None

    def connect(self):
        database = os.path.join(self.server.hostname, self.database.name)
        self._conn = sqlite3.connect(database)

    def execute(self):
        yield from self._conn.execute(self.query.query)

    def disconnect(self):
        try:
            self._conn.close()
        except sqlite3.Error:
            pass
