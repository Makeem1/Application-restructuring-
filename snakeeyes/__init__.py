from flask import Flask


from snakeeyes.contact import contact
from snakeeyes.page import page 
from snakeeyes.user import user
from snakeeyes.admin import admin 
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

    app.register_blueprint(contact)
    app.register_blueprint(page)
    app.register_blueprint(user)
    app.register_blueprint(admin)

    extension(app)

    return app


def extension(app):
    Csrf.init_app(app)
    mail.init_app(app)
    debug_toolbar.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)