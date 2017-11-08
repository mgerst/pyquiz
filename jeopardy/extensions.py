from flask_debugtoolbar import DebugToolbarExtension
from flask_session import Session
from flask_socketio import SocketIO
from flask_webpack import Webpack


webpack = Webpack()

debug_toolbar = DebugToolbarExtension()

session = Session()

socketio = SocketIO(manage_session=False)
