# -*- coding: utf-8 -*-


class DBTriggerException(Exception):
    pass


class ConfigError(DBTriggerException):
    pass


class UnavailableDialect(DBTriggerException):
    pass
