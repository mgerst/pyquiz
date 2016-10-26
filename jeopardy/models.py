from collections import OrderedDict

import yaml
from flask.ext.socketio import send, emit


class BoardManager(object):
    def __init__(self):
        self.boards = OrderedDict()
        self.board_iter = None
        self.current_board = None

    def load_board(self, filename):
        with open(filename, 'r') as fp:
            data = yaml.load(fp)

            for board in data['boards']:
                b = Board(board['order'])
                if board['order'] in self.boards:
                    raise Exception("Can't have multiple boards with the same order")

                b.load_categories(board['categories'])
                self.boards[board['order']] = b

    def init_boards(self):
        self.board_iter = iter(self.boards)

    def next_board(self):
        self.current_board = next(self.board_iter)
        emit('switch.board', {'id': self.current_board})


class Board(object):
    nextid = 1

    def __init__(self, id):
        self.categories = []
        self.teams = []
        self.id = id

    def add_category(self, name):
        ct = Category(self.nextid, name)
        ct.board = self

        self.categories.append(ct)
        self.nextid += 1

        return ct

    def load_categories(self, categories):
        for category in categories:
            ct = self.add_category(category['name'])


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
