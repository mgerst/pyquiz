=======
Running
=======

----------
Dev Server
----------
When running the development server, you need to run both the webpack dev server ***and*** the flask dev server. You will
need to run the following commands in one terminal:

.. code-block:: bash

    export FLASK_APP=jeopardy/web.py
    export FLASK_DEBUG=1
    flask run

and the following in another terminal:

.. code-block:: bash

    npm run dev

.. warning::

   Never run the flask dev server in production.

You may now browse to http://localhost:5000 to view the app. Any changes you make to the javascript/Vue files will be
hot reloaded and take effect immediately.

----------
Production
----------
To run the server in "production" mode, you can simply run:

.. code-block:: bash

    python manage.py run_server

This will build the static assets and start the server. PyQuiz will now be listening on ``0.0.0.0:5000``.
