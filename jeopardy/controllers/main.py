import time

from flask import Blueprint, render_template, request, redirect, session
from flask_socketio import emit
from redis import StrictRedis

from jeopardy.extensions import socketio
from jeopardy.models import BoardManager, Team
from jeopardy.utils import team_required, admin_required

from .utils import get_team_list, send_identity

bm = None  # type: BoardManager
redis = None  # type: StrictRedis


class MainBlueprint(Blueprint):
    def register(self, app, options, first_registration=False):
        global bm, redis

        print("Registered main blueprint")

        bm = app.config.get('BOARD_MANAGER')  # type: BoardManager
        redis = app.config.get('REDIS', None)

        if redis:
            bm._redis = redis

        super().register(app, options, first_registration)


main = MainBlueprint('main', __name__)


@main.route('/')
def index():
    return render_template('app.html')


@main.route('/session/clear')
def clear_session():
    session.clear()
    return redirect('/')


@socketio.on('whoami')
def whoami():
    send_identity()

    emit('game.state', {
        'state': bm.state,
    })

    logged_in = session.get('logged_in', False)
    if not logged_in:
        teams = get_team_list(bm)
        emit('team.list', {'teams': teams})


@socketio.on('team.join')
def team_join(data):
    pass
