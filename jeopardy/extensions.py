from flask_debugtoolbar import DebugToolbarExtension
from flask_assets import Environment
from flask_socketio import SocketIO


# init flask assets
assets_env = Environment()

debug_toolbar = DebugToolbarExtension()

socketio = SocketIO()
