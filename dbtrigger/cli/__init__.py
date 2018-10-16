# -*- coding: utf-8 -*-

from .database import DatabaseCli
from .query import QueryCli
from .server import ServerCli

cli = {
    'database': DatabaseCli(),
    'query': QueryCli(),
    'server': ServerCli(),
}
