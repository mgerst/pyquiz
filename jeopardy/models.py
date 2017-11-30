import json
import logging
import sys
from collections import OrderedDict

import yaml
from flask import session
from redis.client import StrictRedis

from jeopardy.extensions import socketio

logger = logging.getLogger(__name__)


class Question(object):
    def __init__(self, id, value, question, answer, daily_double=False, type="text"):
        self.id = id
        self.value = value
        self.question = question
        self.answer = answer
        self.daily_double = daily_double
        self.visible = True
        self.category = None
        self.type = type

        # Daily Double Stuff
        self.double_team = None
        self.wager = None

    def as_dict(self, sanitized=False):
        ret = {
            'id': self.id,
            'value': self.value,
            'category': self.category.id,
            'visible': self.visible,
        }

        if session.get('admin', False):
            if not sanitized:
                ret.update({
                    'question': self.question,
                    'answer': self.answer,
                    'daily_double': self.daily_double,
                })

        return ret

    def persist(self, r: StrictRedis):
        r.hset("quiz:board:{}:questions".format(self.category.board.id), "{}-{}".format(self.category.id, self.id),
               str(self.visible))

    def load(self, r: StrictRedis):
        active = r.hget("quiz:board:{}:questions".format(self.category.board.id),
                        "{}-{}".format(self.category.id, self.id))
        if active is None:
            self.visible = True
        else:
            self.visible = active.decode('utf-8') == 'True'

        if not self.visible:
            socketio.emit('question.hide', {'category': self.category.id, 'id': self.id})


class Category(object):
    nextid = 1

    def __init__(self, id, name):
        self.id = id
        self.items = []
        self.name = name
        self.board = None

    def add_question(self, value, question, answer, dd=False, type="text"):
        bl = Question(self.nextid, value, question, answer, dd, type)
        bl.category = self

        self.items.append(bl)
        self.nextid += 1

        return bl

    def load_questions(self, questions):
        for question in questions:
            bl = self.add_question(question['value'], question['clue'], question['answer'], question['daily_double'],
                                   question['type'])

    def get_question(self, id: int) -> Question:
        return self.items[id - 1]

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'questions': [ques.as_dict() for ques in self.items],
        }

    def load(self, r: StrictRedis):
        for q in self.items:
            q.load(r)


class Board(object):
    nextid = 1

    TYPE_STANDARD = 'standard'
    TYPE_FINAL = 'final'

    def __init__(self, id, name, type=TYPE_STANDARD):
        self.categories = []
        self.id = id
        self.name = name
        self.type = type

    def add_category(self, name):
        ct = Category(self.nextid, name)
        ct.board = self

        self.categories.append(ct)
        self.nextid += 1

        return ct

    def load_categories(self, categories):
        for category in categories:
            ct = self.add_category(category['name'])
            ct.load_questions(category['questions'])

    def get_category(self, id: int) -> Category:
        return self.categories[id - 1]

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'categories': [cat.as_dict() for cat in self.categories],
            'shape': self.shape,
        }

    def load(self, r: StrictRedis):
        for category in self.categories:
            category.load(r)

    @property
    def shape(self):
        width = len(self.categories)
        height = max(len(c.items) for c in self.categories)
        return {
            'width': width,
            'height': height,
        }


class BoardManager(object):
    STATE_WAITING = 'waiting'
    STATE_PLAYING = 'playing'
    STATE_FINISHED = 'finished'

    def __init__(self):
        self.boards = OrderedDict()
        self.board_iter = None
        self.current_board = None
        self.current_question = None  # type: Question
        self.teams = {}
        self.admin_pw = ""
        self.num_teams = None
        self.buzzer = None
        self._redis = None
        self.state = BoardManager.STATE_WAITING

    def claim_team(self, name: str, id: int, key: str, redis: StrictRedis):
        team = Team(id, name, key)
        self.teams[id] = team

        print("About to persist")
        if redis:
            print("Persisting")
            self.persist(redis)
        print("persisted")

    def team_exists(self, id):
        return id in self.teams

    def validate_team(self, id, key):
        if id in self.teams:
            if self.teams[id].key == key:
                return True
        return False

    def validate_admin(self, password):
        return password == self.admin_pw

    def load_board(self, filename):
        with open(filename, 'r') as fp:
            logger.info("Loading Jeopardy")
            data = yaml.safe_load(fp)
            try:
                self.admin_pw = data['password']
            except KeyError:
                print("Need to set `password` in board.yml.")
                sys.exit()

            try:
                self.num_teams = data['teams']
            except KeyError:
                print("Need to set `teams` in board.yml.")
                sys.exit()

            for board in data['boards']:
                logger.debug("Loading board %d", board['order'])
                b = Board(board['order'], board['name'])
                if board['order'] in self.boards:
                    raise Exception("Can't have multiple boards with the same order")

                logger.debug("Loading categories for board %d", board['order'])
                b.load_categories(board['categories'])
                self.boards[board['order']] = b

        if self._redis:
            self.load(self._redis)

    def init_boards(self):
        self.board_iter = iter(self.boards)

    def next_board(self):
        try:
            self.current_board = next(self.board_iter)
            socketio.emit('board.current', {'id': self.current_board})
        except StopIteration:
            winner = None
            max = 0

            for team in self.teams.values():
                if team.score > max:
                    max = team.score
                    winner = team
            socketio.emit('game.end', {'winner': winner.as_dict()})

    @property
    def current(self) -> Board:
        if not self.current_board:
            self.next_board()

        if self.current_board not in self.boards:
            raise RuntimeWarning("Current board {} not in boards".format(self.current_board))
        return self.boards[self.current_board]

    def persist(self, r: StrictRedis):
        print("Writing board manager to redis")
        for team in self.teams.values():
            team.persist(r)

    def load(self, r: StrictRedis):
        result = r.smembers("quiz:teams")
        for i in result:
            i = int(i)
            t = Team.load(r, i)
            self.teams[i] = t

        for b in self.boards.values():
            b.load(r)


class Team(object):
    def __init__(self, id, name, key, score=0):
        self.id = id
        self.name = name
        self.key = key
        self.score = score

    def as_dict(self):
        return {'id': self.id, 'name': self.name, 'score': self.score}

    def persist(self, r: StrictRedis):
        print("Writing team to redis")
        r.sadd("quiz:teams", self.id)
        r.hset("quiz:team", self.id, json.dumps({
            'id': self.id,
            'name': self.name,
            'key': self.key,
            'score': self.score}
        ))

    @classmethod
    def load(cls, r: StrictRedis, id: int) -> 'Team':
        result = r.hget("quiz:team", id)
        result = json.loads(result.decode('utf-8'))

        return cls(int(result['id']), result['name'], result['key'], int(result['score']))
