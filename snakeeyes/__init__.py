from flask import Flask

from werkzeug.middleware.proxy_fix import ProxyFix
from snakeeyes.blueprints.contact import contact
from snakeeyes.blueprints.page import page 
from snakeeyes.blueprints.user import user
from snakeeyes.blueprints.admin import admin 
from snakeeyes.blueprints.error_page import error
from snakeeyes.extensions import Csrf, mail, debug_toolbar, db, login_manager

login_manager.login_view = 'user.login'
login_manager.login_message = 'You need to login to access this page'
login_manager.login_message_category = 'info'
login_manager.session_protection = 'strong'
login_manager.refresh_view = 'user.login'
login_manager.needs_refresh_message = "To protect your account, please reauthenticate to access this page."
login_manager.needs_refresh_message_category = "info"

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

    app.logger.setLevel(app.config['LOG_LEVEL'])

    middleware(app)
    exception_handler(app)
    app.register_blueprint(contact)
    app.register_blueprint(page)
    app.register_blueprint(user)
    app.register_blueprint(admin)
    app.register_blueprint(error)

    extension(app)

    return app


def extension(app):
    Csrf.init_app(app)
    mail.init_app(app)
    debug_toolbar.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)


def middleware(app):
    """This help to get the real ip address when using proxy server like nginx in production,
        it serve as a gateway between flask wsgi
    """

    app.wsgi_app = ProxyFix(app.wsgi_app)

    return None

def exception_handler(app):
    """
    Register 0 or more exception handlers (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    mail_handler = SMTPHandler((app.config.get('MAIL_SERVER'),
                                app.config.get('MAIL_PORT')),
                               app.config.get('MAIL_USERNAME'),
                               [app.config.get('MAIL_USERNAME')],
                               '[Exception handler] A 5xx was thrown',
                               (app.config.get('MAIL_USERNAME'),
                                app.config.get('MAIL_PASSWORD')),
                               secure=())

    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(logging.Formatter("""
    Time:               %(asctime)s
    Message type:       %(levelname)s


    Message:

    %(message)s
    """))
    app.logger.addHandler(mail_handler)

    return None
