# -*- coding: utf-8 -*-

from abc import abstractmethod

from ..models import Query


class Runner:

    def __init__(self, query: Query):
        self.query = query
        self.database = query.database
        self.server = query.database.server

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    def run(self):
        self.connect()
        try:
            yield from self.execute()
        finally:
            self.disconnect()
