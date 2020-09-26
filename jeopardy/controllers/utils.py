from flask import session
from flask_socketio import emit

from ..models import BoardManager, Board


def get_team_list(bm: BoardManager):
    teams = []
    for i in range(1, bm.num_teams+1):
        if bm.team_exists(i):
            team = bm.teams[i]
            teams.append({
                'id': i,
                'name': team.name,
                'taken': True,
                'score': 0,
            })
    return teams


def send_identity():
    emit('youAre', {
        'admin': session.get('admin', False),
        'team': session.get('team', None),
        'logged_in': session.get('logged_in', False),
    })


def send_team_list(bm: BoardManager, broadcast: bool = False):
    teams = get_team_list(bm)
    emit('team.list', {'teams': teams, 'max_teams': bm.num_teams}, broadcast=broadcast)


def send_board_current(bm: BoardManager):
    emit('board.current', bm.current.as_dict(), broadcast=True)


def send_board_switch(board: Board):
    emit('board.switch', {
        'id': board.id,
        'name': board.name,
        'type': board.type,
    }, broadcast=True)
