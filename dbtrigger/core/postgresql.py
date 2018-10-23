# -*- coding: utf-8 -*-

import os
import psycopg2

from .abstract import Runner
from ..models import Query


class PostgresqlRunner(Runner):

    def __init__(self, query: Query):
        super().__init__(query)
        self._conn = None

    def connect(self):
        self._conn = psycopg2.connect(
            host=self.server.hostname,
            port=self.server.port,
            database=self.database.name,
            user=self.database.username,
            password=self.database.password,
        )

    def execute(self):
        with self._conn.cursor() as cursor:
            cursor.execute(self.query.query)
            yield from cursor.fetchall()

    def disconnect(self):
        try:
            self._conn.close()
        except psycopg2.Error:
            pass
