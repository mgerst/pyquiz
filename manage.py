#!/usr/bin/env python

import os
import subprocess

import redis
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
@manager.option('--skip-npm', dest='skip_npm', action='store_true', default=False)
def run_server(boards, skip_npm):
    bm = app.config.get('BOARD_MANAGER')
    bm.load_board(boards)
    bm.init_boards()

    if not skip_npm:
        subprocess.call(['npm', 'run', 'build'])

    from jeopardy.extensions import socketio
    socketio.run(app, host='0.0.0.0')


@manager.command
def lint():
    subprocess.call(["flake8", "jeopardy"])


@manager.command
def test():
    subprocess.call(["py.test"])


@manager.command
def clear_redis():
    r = redis.StrictRedis(host='localhost', db=2)
    # Redis doesn't support wildcard deletes apparently.
    # https://stackoverflow.com/questions/4006324/how-to-atomically-delete-keys-matching-a-pattern-using-redis
    r.eval("return redis.call('del', unpack(redis.call('keys', ARGV[1])))", 0, "quiz:*")
    r.eval("return redis.call('del', unpack(redis.call('keys', ARGV[1])))", 0, "session:*")


if __name__ == "__main__":
    manager.run()
