from functools import wraps
from flask import session, redirect


def team_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if 'team' in session:
            return f(*args, **kwargs)
        return redirect('/')

    return inner


def admin_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if 'admin' in session and session['admin']:
            return f(*args, **kwargs)
        return redirect('/')

    return inner


def login_required(f):
    @wraps(f)
    def inner(*args, **kwargs):
        if 'logged_in' in session and session['logged_in']:
            return f(*args, **kwargs)
        return redirect('/')

    return inner
