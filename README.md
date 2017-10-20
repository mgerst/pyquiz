Py Quiz
=======
A python implementation of Jeopardy.

Installation
============
Install the dependencies:

    pip install -r requirements.txt

Modify (or create your own) `board.yml` file and run the server (for "production"):

    python manage.py run_server
    
Running the Dev Server
======================
When running the development server, you need to run both the webpack dev server ***and*** the flask dev server.
You will need to run the following commands in one terminal:

    export FLASK_APP=jeopardy.web
    export FLASK_DEBUG=1
    flask run

and the following in another terminal:

    npm run dev

You can then browse the http://localhost:5000 to view the app. Any changes you make to the javascript/Vue files
will be hot reloaded and take effect immediately.
