# -*- coding: utf-8 -*-

import pytest

import dbtrigger.config


@pytest.fixture(scope="function", autouse=True)
def settings(monkeypatch, tmpdir):
    monkeypatch.setattr(dbtrigger.config.settings, 'CONFIG_BASE_PATH', tmpdir.strpath)
    dbtrigger.config.settings.load_config()
    yield
    dbtrigger.config.settings.load_config()

