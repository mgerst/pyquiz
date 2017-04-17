from flask import Blueprint, render_template, flash, request, redirect, url_for, session
from flask_socketio import emit

from jeopardy.extensions import socketio
from jeopardy.models import BoardManager
from jeopardy.utils import team_required, login_required, admin_required

import time

bm = None  # type: BoardManager


class MainBlueprint(Blueprint):
    def register(self, app, options, first_registration=False):
        global bm

        print("Registered main blueprint")

        bm = app.config.get('BOARD_MANAGER')
        super().register(app, options, first_registration)


main = MainBlueprint('main', __name__)


@main.route('/board')
@login_required
def board():
    return render_template('board.html')


@main.route('/')
def index():
    teams = {}
    for i in range(1, 5):
        if bm.team_exists(i):
            teams[i] = bm.teams[i].name
        else:
            teams[i] = None
    return render_template('index.html', teams=teams)


@main.route('/play/<team>', methods=['GET', 'POST'])
def claim_team(team):
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
            bm.claim_team(request.form['name'], team, request.form['key'])
            return redirect('/board')
        return redirect('/play/{}'.format(team))


@socketio.on('whoami')
def whoami():
    emit('whoami', {
        'admin': session.get('admin', False),
        'team': session.get('team', None),
        'logged_in': session.get('logged_in', False),
    })


@socketio.on('board.current')
def on_board_current():
    cur_board = bm.current
    emit('board.current', cur_board.as_dict())


@socketio.on('question.open')
@admin_required
def on_question_open(data):
    cat_id = int(data['category'])
    question_id = int(data['id'])

    print("Opening question {}-{}".format(cat_id, question_id))

    cat = bm.current.get_category(cat_id)
    question = cat.get_question(question_id)
    bm.current_question = question

    emit('question.open', question.as_dict(), broadcast=True)


@socketio.on('question.close')
@admin_required
def on_question_close(data):
    remove = data['remove']
    question = bm.current_question
    bm.current_question = None

    ret_data = {
        'question': question.as_dict(),
        'remove': remove,
    }

    emit('question.close', ret_data, broadcast=True)


@socketio.on('buzzer.clicked')
@team_required
def buzzer_clicked(data):
    emit('buzzer.clicked', {'team': data['team']}, broadcast=True)


@socketio.on('buzzer.open')
@admin_required
def buzzer_open():
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

    team = bm.teams[data['team']]
    team.score += bm.current_question.value
    emit('team.award', {'team': team.id, 'score': team.score}, broadcast=True)
