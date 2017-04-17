from flask import Blueprint, render_template, flash, request, redirect, url_for, session
from flask_socketio import emit

from jeopardy.extensions import socketio
from jeopardy.models import BoardManager
from jeopardy.utils import team_required, login_required, admin_required

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
