# -*- coding: utf-8 -*-

from .database import DatabaseCli
from .server import ServerCli

cli = {
    'database': DatabaseCli(),
    'server': ServerCli(),
}
