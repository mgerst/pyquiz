#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest


@pytest.mark.usefixtures('testapp')
class TestURLs:
    def test_home(self, testapp):
        """ Tests if the home page loads """

        rv = testapp.get('/')
        assert rv.status_code == 200
