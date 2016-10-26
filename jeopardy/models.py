from collections import OrderedDict
import logging

import yaml
from flask_socketio import send, emit


logger = logging.getLogger(__name__)


class BoardManager(object):
    def __init__(self):
        self.boards = OrderedDict()
        self.board_iter = None
        self.current_board = None

    def load_board(self, filename):
        with open(filename, 'r') as fp:
            logger.info("Loading Jeopardy")
            data = yaml.load(fp)

            for board in data['boards']:
                logger.debug("Loading board %d", board['order'])
                b = Board(board['order'], board['name'])
                if board['order'] in self.boards:
                    raise Exception("Can't have multiple boards with the same order")

                logger.debug("Loadinb categories for board %d", board['order'])
                b.load_categories(board['categories'])
                self.boards[board['order']] = b

    def init_boards(self):
        self.board_iter = iter(self.boards)

    def next_board(self):
        try:
            self.current_board = next(self.board_iter)
            emit('board.switch', {'id': self.current_board})
        except StopIteration:
            emit('game.end')

    @property
    def current(self):
        if not self.current_board:
            self.next_board()

        if self.current_board not in self.boards:
            raise RuntimeWarning("Current board {} not in boards".format(self.current_board))
        return self.boards[self.current_board]


class Board(object):
    nextid = 1

    def __init__(self, id, name):
        self.categories = []
        self.teams = []
        self.id = id
        self.name = name

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

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'teams': [team.as_dict() for team in self.teams],
            'categories': [cat.as_dict() for cat in self.categories],
        }


class Category(object):
    nextid = 1

    def __init__(self, id, name):
        self.id = id
        self.items = []
        self.name = name
        self.board = None

    def add_question(self, value, question, answer, dd=False):
        bl = Question(self.nextid, value, question, answer, dd)
        bl.category = self

        self.items.append(bl)
        self.nextid += 1

        return bl

    def load_questions(self, questions):
        for question in questions:
            bl = self.add_question(question['value'], question['clue'], question['answer'], question['daily_double'])

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'questions': [ques.as_dict() for ques in self.items],
        }


class Question(object):
    def __init__(self, id, value, question, answer, daily_double=False):
        self.id = id
        self.value = value
        self.question = question
        self.answer = answer
        self.daily_double = daily_double
        self.visible = True
        self.category = None

    def mark_answered(self):
        emit('close-item', {'id': self.id, 'category': self.category.id})

    def as_dict(self):
        return {
            'id': self.id,
            'value': self.value,
            'question': self.question,
            'answer': self.answer,
            'daily_double': self.daily_double,
            'visible': self.visible,
        }


class Team(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.score = 0

    def as_dict(self):
        return {'id': self.id, 'name': self.name, 'score': self.score}
