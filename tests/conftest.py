import pytest

from jeopardy import create_app


@pytest.fixture
def testapp(request):
    app = create_app('jeopardy.settings.TestConfig')
    client = app.test_client()

    return client
