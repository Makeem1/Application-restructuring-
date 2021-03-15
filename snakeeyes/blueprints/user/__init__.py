from flask import Blueprint


user = Blueprint('user', __name__, template_folder='templates')


from snakeeyes.blueprints.user import views
