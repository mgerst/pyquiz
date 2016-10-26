from flask_debugtoolbar import DebugToolbarExtension
from flask_assets import Environment


# init flask assets
assets_env = Environment()

debug_toolbar = DebugToolbarExtension()

