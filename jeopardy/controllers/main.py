import time

from flask import Blueprint, render_template, request, redirect, session
from flask_socketio import emit
from redis import StrictRedis

from jeopardy.extensions import socketio
from jeopardy.models import BoardManager, Team
from jeopardy.utils import team_required, admin_required

from .utils import get_team_list, send_identity, send_board_current

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
    observer = 'true' if 'observer' in request.args else 'false'
    return render_template('app.html', admin=admin, observer=observer)


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

    if session.get('admin', False) and bm.current_board:
        send_board_current(bm)

    if bm.current_question:
        question = bm.current_question
        emit('question.open', {
            'clue': question.question,
            'value': question.value,
            'question': question.id,
            'category': question.category.id,
        })


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

    if bm.state == BoardManager.STATE_PLAYING:
        send_board_current(bm)


@socketio.on('team.buzz')
@team_required
def team_buzz():
    if not bm.buzzer:
        bm.buzzer = True
        team = session.get('team')
        emit('buzzer.close', {'team': team}, broadcast=True)


@socketio.on('team.award')
@admin_required
def team_award(data):
    team_id = data['id']
    amount = data['amount']

    if not bm.team_exists(team_id):
        emit('error', {'error': 'Invalid team', 'team': team_id})
        return

    team = bm.teams[team_id]
    if bm.current_question.daily_double:
        # In the daily double case, the amount will be +1 or -1
        # as a way to handle award/detract.
        team.score += amount * bm.current_question.wager
    else:
        team.score += amount

    if redis:
        team.persist(redis)

    emit('team.score', {'team': team_id, 'score': team.score}, broadcast=True)


@socketio.on('team.detract')
@admin_required
def team_detract(data):
    data['amount'] = -data['amount']
    # Don't really need to repeat the logic here.
    team_award(data)


@socketio.on('admin.login')
def admin_login(data):
    password = data['password']

    if bm.validate_admin(password):
        session['admin'] = True
        session['logged_in'] = True
        session.modified = True
        send_identity()
        if bm.current_board:
            send_board_current(bm)
    else:
        emit('error', {'error': 'Invalid admin login'})


@socketio.on('game.start')
@admin_required
def game_start():
    bm.state = BoardManager.STATE_PLAYING
    emit('game.state', {'state': bm.state}, broadcast=True)

    board = bm.current
    emit('board.switch', {
        'id': board.id,
        'name': board.name,
        'type': board.type,
    }, broadcast=True)
    send_board_current(bm)


@socketio.on('board.current')
def board_current():
    send_board_current(bm)


@socketio.on('question.open')
@admin_required
def question_open(data):
    question_id = data['question']
    category_id = data['category']

    category = bm.current.get_category(category_id)
    question = category.get_question(question_id)
    bm.current_question = question

    ret = {
        'clue': question.question,
        'value': question.value,
        'question': question_id,
        'category': category_id,
        'daily_double': question.daily_double,
    }
    emit('question.open', ret, broadcast=True)


@socketio.on('question.reveal')
@admin_required
def question_reveal():
    question = bm.current_question.answer
    emit('question.reveal', {'answer': question}, broadcast=True)


@socketio.on('question.close')
@admin_required
def question_close():
    question = bm.current_question
    if question:
        question.visible = False
        question.persist(redis)

    bm.current_question = None
    emit('question.close', broadcast=True)


@socketio.on('question.wager')
@admin_required
def question_wager(data):
    question = bm.current_question
    question.double_team = int(data['team'])
    question.wager = int(data['wager'])
    emit('question.wager', broadcast=True)
    emit('buzzer.close', {'team': question.double_team}, broadcast=True)


@socketio.on('buzzer.open')
@admin_required
def buzzer_open():
    bm.buzzer = False
    emit('buzzer.open', broadcast=True)

