from flask_assets import Bundle

common_css = Bundle(
    'css/jeopardy.css',
    filters='cssmin',
    output='public/css/common.css'
)

common_js = Bundle(
    'js/jquery-3.2.1.min.js',
    'js/socket.io.min.js',
    Bundle(
        'js/main.js',
        filters='jsmin'
    ),
    output='public/js/common.js'
)
