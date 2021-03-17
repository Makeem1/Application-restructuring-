from snakeeyes.blueprints.error_page import error
from flask import render_template

@error.app_errorhandler(404)
def page_not_found(e):
    return render_template('error/error_404.html'), 404

@error.app_errorhandler(500)
def ser_error(e):
    return render_template('error/error_500.html'), 500
    