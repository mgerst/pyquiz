#!/usr/bin/env python

import os
import subprocess

from flask_script import Manager, Server
from flask_script.commands import ShowUrls, Clean
from jeopardy import create_app

# default to dev config because no one should use this in
# production anyway
from jeopardy.models import BoardManager

env = os.environ.get('JEOPARDY_ENV', 'dev')
app = create_app('jeopardy.settings.%sConfig' % env.capitalize())

manager = Manager(app)
manager.add_command("show-urls", ShowUrls())
manager.add_command("clean", Clean())


@manager.option('-b', '--boards', dest='boards', default='board.yml')
def run_server(boards):
    bm = app.config.get('BOARD_MANAGER')
    bm.load_board(boards)
    bm.init_boards()

    from jeopardy.extensions import socketio
    socketio.run(app)


@manager.command
def lint():
    subprocess.call(["flake8", "jeopardy"])


@manager.command
def test():
    subprocess.call(["py.test"])

if __name__ == "__main__":
    manager.run()
