import os

from jeopardy import create_app

app = create_app('jeopardy.settings.ProdConfig')
board = os.environ.get('QUIZ_BOARD', 'board.yml')

bm = app.config.get('BOARD_MANAGER')
bm.load_board(board)
bm.init_boards()

from jeopardy.extensions import socketio
socketio.run(app)