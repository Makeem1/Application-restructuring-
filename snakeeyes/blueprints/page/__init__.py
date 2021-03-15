from flask import Blueprint

page = Blueprint('page', __name__, template_folder='templates')

from snakeeyes.page import views 