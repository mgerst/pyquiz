#!/usr/bin/env python

import os

from flask_script import Manager, Server
from flask_script.commands import ShowUrls, Clean
from jeopardy import create_app

# default to dev config because no one should use this in
# production anyway
env = os.environ.get('JEOPARDY_ENV', 'dev')
app = create_app('jeopardy.settings.%sConfig' % env.capitalize())

manager = Manager(app)
manager.add_command("server", Server())
manager.add_command("show-urls", ShowUrls())
manager.add_command("clean", Clean())

if __name__ == "__main__":
    manager.run()
