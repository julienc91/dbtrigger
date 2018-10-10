# -*- coding: utf-8 -*-

from dataclasses import dataclass

from .server import Server


@dataclass
class Database:

    identifier: str

    server: Server
    username: str
    password: str
    name: str
