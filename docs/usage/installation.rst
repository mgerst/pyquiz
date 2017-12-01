============
Installation
============
PyQuiz uses npm to manage it's frontend dependencies and pip to handle the backend dependencies. If you do not have
npm/node, you will need to `install it`_ following the directions appropriate for your system. You will also need to
install the python requirements:

.. code-block:: python

   pip install -r requirements.txt

.. note::

   It is highly recommended that you use a `virtualenv`_.

-------------------
System Dependencies
-------------------
There are no system-level dependencies. You will need a `Redis`_ server running, either locally or on another machine.
By default, pyquiz will use redis 3rd logical database (database 2, see the `select command`_). If you are familiar with
Flask, you can use the config objects to configure this option, it is planned to make this easier.

.. _install it: https://nodejs.org/en/download/
.. _virtualenv: https://virtualenv.pypa.io/en/stable/
.. _Redis: https://redis.io/
.. _select command: https://redis.io/commands/select
