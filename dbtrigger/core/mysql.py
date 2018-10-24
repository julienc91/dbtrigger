# -*- coding: utf-8 -*-

import pymysql

from .abstract import Runner
from ..models import Query


class MysqlRunner(Runner):

    def __init__(self, query: Query):
        super().__init__(query)
        self._conn = None

    def connect(self):
        self._conn = pymysql.connect(
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
        except pymysql.MySQLError:
            pass
