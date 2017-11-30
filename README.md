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

    export FLASK_APP=jeopardy/web.py
    export FLASK_DEBUG=1
    flask run

and the following in another terminal:

    npm run dev

You can then browse the http://localhost:5000 to view the app. Any changes you make to the javascript/Vue files
will be hot reloaded and take effect immediately.

Usage
=====
Regular clients may simply browse to `http://the.host.ip.address:5000` and select their team. Admin users may
browse to `http://the.host.ip.address:5000?admin` and click the admin "team" and enter the admin password. The
only difference between the two endpoints is the admin link.

Observers may browse to `http://the.host.ip.address:5000?observer`. This view will always display the current
state of the game, but may not interact with it in any way.

Board File
==========
The board file is written in YAML and is fairly simple. You can see an example in `board.yml`.

Text Clues
----------
Text clues are the default, and are specified like so:

```yaml
...
   questions:
      - clue: Text for the clue
        answer: The correct answer (or question in jeopardy terms)
        value: 100
        daily_double: no
        type: text
```

Image Clues
-----------
Image clues display an image instead of a text clue, the answer is still text. The value of the questions `clue`
key will be used as the `src` attribute for the `img` tag. There is currently no built-in method of serving local
images through pyquiz, but you can convert the image to a `data-uri` if you want something self contained.

```yaml
...
   questions:
       - clue: http://url/to/image
         answer: The correct answer
         value: 100
         daily_double: no
         type: image
```
