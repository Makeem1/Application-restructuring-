from flask import Blueprint

error = Blueprint('error', __name__)

from snakeeyes.blueprints.error_page import views