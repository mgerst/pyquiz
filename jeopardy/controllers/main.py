import time

from flask import Blueprint, render_template, request, redirect, session
from flask_socketio import emit
from redis import StrictRedis

from jeopardy.extensions import socketio
from jeopardy.models import BoardManager, Team
from jeopardy.utils import team_required, admin_required

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


@main.route('/board')
def board():
    teams = dict(bm.teams)

    for i in range(1, bm.num_teams+1):
        if i not in teams:
            teams[i] = Team(i, None, None)

    return render_template('board.html', teams=teams, admin=session.get('admin'))


@main.route('/')
def index():
    teams = {}
    for i in range(1, bm.num_teams+1):
        if bm.team_exists(i):
            teams[i] = bm.teams[i].name
        else:
            teams[i] = None
    return render_template('index.html', teams=teams)


@main.route("/session/clear")
def clear_session():
    session.clear()
    return redirect('/')


@main.route('/play/<int:team>', methods=['GET', 'POST'])
def claim_team(team):
    if bm.num_teams < team < 0:
        return redirect('/')

    if request.method == 'GET':
        if bm.team_exists(team):
            return render_template('rejoin.html', team=team)
        return render_template('login.html', team=team)
    elif request.method == 'POST':
        if bm.team_exists(team):
            if 'key' in request.form and bm.validate_team(team, request.form['key']):
                session['team'] = team
                session['logged_in'] = True
                session.modified = True
                return redirect('/board')
        else:
            session['team'] = team
            session['logged_in'] = True
            session.modified = True
            bm.claim_team(request.form['name'], team, request.form['key'], redis)
            return redirect('/board')
        return redirect('/play/{}'.format(team))


@main.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'GET':
        return render_template('login.html', admin=True)
    if 'password' in request.form and bm.validate_admin(request.form['password']):
        session['admin'] = True
        session['logged_in'] = True
    return redirect('/board')


@socketio.on('whoami')
def whoami():
    emit('you.are', {
        'admin': session.get('admin', False),
        'team': session.get('team', None),
        'logged_in': session.get('logged_in', False),
    })


@socketio.on('board.current')
def on_board_current():
    cur_board = bm.current
    emit('board.current', cur_board.as_dict())


@socketio.on('board.next')
def on_board_next():
    bm.next_board()


@socketio.on('board.persist')
@admin_required
def persist():
    if redis:
        bm.persist(redis)


@socketio.on('question.open')
@admin_required
def on_question_open(data):
    cat_id = int(data['category'])
    question_id = int(data['id'])

    cat = bm.current.get_category(cat_id)
    question = cat.get_question(question_id)
    bm.current_question = question

    ret = question.as_dict(True)
    ret['daily_double'] = question.daily_double
    ret['question'] = question.question
    ret['category'] = question.category.id
    question.visible = True

    if 'reopen' in data and data['reopen']:
        question.daily_double = False
        ret['daily_double'] = False

    if question.daily_double:
        del ret['question']
        emit('double.open', ret, broadcast=True)
    else:
        emit('question.open', ret, broadcast=True)


@socketio.on('double.wager')
@admin_required
def on_double(data):
    question = bm.current_question
    question.double_team = data['team']
    question.wager = int(data['wager'])

    emit('double.start', {'team': data['team'], 'question': question.question}, broadcast=True)


@socketio.on('correct.answer')
@admin_required
def show_correct_answer():
    question = bm.current_question

    ret_data = {
        'answer': question.answer
    }
    emit('correct.answer', ret_data, broadcast=True)


@socketio.on('question.close')
@admin_required
def on_question_close(data):
    remove = data['remove']
    question = bm.current_question
    if remove:
        question.visible = False
        question.persist(redis)
    bm.current_question = None

    ret_data = {
        'question': question.as_dict(),
        'remove': remove,
    }

    emit('question.close', ret_data, broadcast=True)


@socketio.on('buzzer.clicked')
@team_required
def buzzer_clicked():
    if not bm.buzzer:
        bm.buzzer = True
        emit('buzzer.clicked', {'team': session['team']}, broadcast=True)


@socketio.on('buzzer.open')
@admin_required
def buzzer_open():
    bm.buzzer = False
    emit('buzzer.opened', {'start': int(time.time())}, broadcast=True)


@socketio.on('buzzer.close')
@admin_required
def buzzer_close():
    emit('buzzer.closed', {'end': int(time.time())}, broadcast=True)


@socketio.on('team.award')
@admin_required
def team_award(data):
    if not bm.team_exists(data['team']):
        emit('error', {'error': "Team does not exist", 'value': data['team']})

    team = bm.teams[int(data['team'])]
    if data['correct']:
        if bm.current_question.daily_double:
            team.score += bm.current_question.wager
            bm.current_question.wager = None
        else:
            team.score += bm.current_question.value
    else:
        if bm.current_question.daily_double:
            team.score -= bm.current_question.wager
            bm.current_question.wager = None
        else:
            team.score -= bm.current_question.value

    if redis:
        team.persist(redis)

    emit('team.award', {'team': team.id, 'score': team.score}, broadcast=True)
