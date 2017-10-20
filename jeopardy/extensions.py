from flask_debugtoolbar import DebugToolbarExtension
from flask_socketio import SocketIO
from flask_webpack import Webpack


webpack = Webpack()

debug_toolbar = DebugToolbarExtension()

socketio = SocketIO()
