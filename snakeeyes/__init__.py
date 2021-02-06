from flask import Flask

from celery import Celery


from snakeeyes.contact import contact
from snakeeyes.page import page 
from snakeeyes.extensions import Csrf, mail, debug_toolbar

CELERY_TASK_LIST = [ 'snakeeyes.email', ] 

def create_celery_app(app=None):

    app = app or create_app

    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'],
        include=CELERY_TASK_LIST
    )

    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_app(override_settings=None):
    """
    Create a Flask application using the app factory pattern.

    :return: Flask app
    
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    if override_settings:
        app.config.update(override_settings)

    app.register_blueprint(contact)
    app.register_blueprint(page)

    extension(app)



    return app


def extension(app):
    Csrf.init_app(app)
    mail.init_app(app)
    debug_toolbar.init_app(app)