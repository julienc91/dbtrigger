# -*- coding: utf-8 -*-

import appdirs

from .config import Settings


settings = Settings(appdirs.user_data_dir('dbtrigger'))
