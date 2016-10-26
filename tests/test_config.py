#!/usr/bin/env python
# -*- coding: utf-8 -*-
from jeopardy import create_app


class TestConfig:
    def test_dev_config(self):
        """ Tests if the development config loads correctly """

        app = create_app('jeopardy.settings.DevConfig')

        assert app.config['DEBUG'] is True

    def test_test_config(self):
        """ Tests if the test config loads correctly """

        app = create_app('jeopardy.settings.TestConfig')

        assert app.config['DEBUG'] is True

    def test_prod_config(self):
        """ Tests if the production config loads correctly """

        app = create_app('jeopardy.settings.ProdConfig')

        assert app.config['DEBUG'] is False
