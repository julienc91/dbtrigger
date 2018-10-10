# -*- coding: utf-8 -*-

import fire

from dbtrigger.cli import ServerCli


if __name__ == '__main__':
    fire.Fire({
        'server': ServerCli()
    })
