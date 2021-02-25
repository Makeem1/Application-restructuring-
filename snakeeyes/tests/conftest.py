import pytest
from config import settings
from snakeeyes import create_app
from snakeeyes.extensions import db as _db
from snakeeyes.user.models import User



@pytest.fixture(scope = 'session')
def app(override_settings=None):
    # Creating an app instamce for db
    db_uri = '{0}_test'.format(settings.SQLALCHEMY_DATABASE_URI)
    param = {
        'DEBUG' : False,
        'TESTING' : True,
        'WTF_CSRF_ENABLED': False,
        'SQLALCHEMY_DATABASE_URI': db_uri
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


pytest.fixture(scope='session')
def db(app):
    """Creating a database instance"""
    _db.drop_all()
    _db.create_all()

    params = {
        'role': 'admin',
        'email': 'admin@local.host',
        'password': 'password',
    }

    admin = User(**params)

    _db.session.add(admin)
    _db.session.commit()

    return _db


@pytest.fixture(scope='function')
def session(db):
    """Creating a function for faster test"""
    db.session.begin_nexted()
    yield db.session
    db.session.rollback() 


@pytest.fixture(scope='session')
def token(db):
    """creating a token test"""
    user = User.find_by_identity('admin@local.host')
    return user.serialize_token()


@pytest.fixture(scope='function')
def user(db):
    db.session.query(User).delete()
    
    users = [
        {
            'role':'admin',
            'email':'admin@local.host',
            'password':'password'
        },
        {
            'active':False,
            'email': 'disabled@local.host',
            'password': 'password'

        }
    ]

    for user in users:
        db.session.add(user)
    db.session.commit()

    return db