import pytest

from snakeeyes import create_app


@pytest.fixture(scope = 'session')
def app(override_settings=None):

    param = {
        'DEBUG' : False,
        'TESTING' : True
    }

    _app = create_app(override_settings=param)


    app_ctx = _app.app_context()
    app_ctx.push()

    yield _app

    app_ctx.pop()


@pytest.fixture(scope='function')
def client(app):
    """
    :test_client(): function helps to run the server without actually running the server for test purpose.

    :client: is passed as a fixture to the test function which will run before the test is run in the test code.
    
    
    """
    return app.test_client()