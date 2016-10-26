from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_socketio import emit

from jeopardy.extensions import socketio
from jeopardy.models import BoardManager

bm = None  # type: BoardManager


class MainBlueprint(Blueprint):
    def register(self, app, options, first_registration=False):
        global bm

        print("Registered main blueprint")

        bm = app.config.get('BOARD_MANAGER')
        super().register(app, options, first_registration)

main = MainBlueprint('main', __name__)


@main.route('/')
def home():
    return render_template('index.html')


@socketio.on('board.current')
def on_board_current():
    cur_board = bm.current
    emit('board.current', cur_board.as_dict())


@socketio.on('question.open')
def on_question_open(data):
    cat_id = int(data['category'])
    question_id = int(data['id'])

    print("Opening question {}-{}".format(cat_id, question_id))

    cat = bm.current.get_category(cat_id)
    question = cat.get_question(question_id)

    emit('question.open', question.as_dict(), broadcast=True)
