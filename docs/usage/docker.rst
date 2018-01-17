==================
Deploy with Docker
==================
If you prefer using docker, pyquiz provides a `docker-compose.yml` file. To run pyquiz with docker you can run the
following command:

.. code-block:: bash

    docker-compose up

This will build and start the docker image. PyQuiz can then be accessed at `http://localhost:5000`. To reset the status
of the game (Teams, board progress, etc.) run the following:

.. code-block:: bash

    docker-compose run --rm web python manage.py clear_redis
