from flask import session
from flask_socketio import emit

from ..models import BoardManager


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
        else:
            teams.append({
                'id': i,
                'name': None,
                'taken': False,
                'score': 0,
            })
    return teams


def send_identity():
    emit('youAre', {
        'admin': session.get('admin', False),
        'team': session.get('team', None),
        'logged_in': session.get('logged_in', False),
    })