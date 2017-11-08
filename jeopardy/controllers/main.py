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
    admin = 'true' if 'admin' in request.args else 'false'
    return render_template('app.html', admin=admin)


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
    team_id = data['id']

    if bm.team_exists(team_id):
        if bm.validate_team(team_id, data['password']):
            session['team'] = team_id
            session['logged_in'] = True
            session.modified = True

            send_identity()
            emit('team.joined', {
                'team': team_id,
                'name': bm.teams[team_id].name,
            }, broadcast=True)
        else:
            emit('error', {
                'error': 'Invalid team or re-join password',
            })
    else:
        session['team'] = team_id
        session['logged_in'] = True
        session.modified = True
        bm.claim_team(data['name'], team_id, data['password'], redis)


@socketio.on('admin.login')
def admin_login(data):
    password = data['password']

    if bm.validate_admin(password):
        session['admin'] = True
        session['logged_in'] = True
        session.modified = True
        send_identity()
    else:
        emit('error', {'error': 'Invalid admin login'})


@socketio.on('game.start')
def game_start():
    bm.state = BoardManager.STATE_PLAYING
    emit('game.state', {'state': bm.state}, broadcast=True)
