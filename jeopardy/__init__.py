#!/usr/bin/env python
import redis
from flask import Flask
from webassets.loaders import PythonLoader as PythonAssetsLoader

from jeopardy import assets
from jeopardy.controllers.main import main

from jeopardy.extensions import (
    assets_env,
    debug_toolbar,
    socketio
)
from jeopardy.models import BoardManager


def create_app(object_name):
    """
    A flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object,
                     e.g. jeopardy.settings.ProdConfig
    """

    app = Flask(__name__)

    app.config.from_object(object_name)

    bm = BoardManager()
    app.config['BOARD_MANAGER'] = bm
    # Redis is optional
    try:
        r = redis.StrictRedis(host=app.config['REDIS_HOST'], db=app.config['REDIS_DB'])
        app.config['REDIS'] = r
        print("Connected to redis")
    except:
        app.config['REDIS'] = None

    # initialize the debug tool bar
    debug_toolbar.init_app(app)

    # Import and register the different asset bundles
    assets_env.init_app(app)
    assets_loader = PythonAssetsLoader(assets)
    for name, bundle in assets_loader.load_bundles().items():
        assets_env.register(name, bundle)

    socketio.init_app(app)

    # register out blueprints
    app.register_blueprint(main)

    return app
