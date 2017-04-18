from flask_assets import Bundle

common_css = Bundle(
    'css/jeopardy.css',
    'css/print.css',
    filters='cssmin',
    output='public/css/common.css'
)

common_js = Bundle(
    'js/jquery-3.2.1.min.js',
    'js/socket.io.min.js',
    Bundle(
        'js/jeopardy.js',
        'js/main.js',
        filters='jsmin'
    ),
    output='public/js/common.js'
)
