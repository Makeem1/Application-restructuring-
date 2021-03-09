from flask import render_template
from snakeeyes.admin import admin
from flask_login import login_required
from snakeeyes.admin.decorators import role_required
from snakeeyes.admin.models import DashBoard
from snakeeyes.admin.forms import SearchForm



@admin.before_request
@login_required
@role_required('admin')
def before_request():
    """Function to monitor admin page"""
    pass


@admin.route('')
def dashboard():
    group_and_count_users = DashBoard.group_and_count_users()
    return render_template('admin/page/admin.html', group_and_count_users = group_and_count_users)


@admin.route('/users')
def users():
    """Fucntion to list all users in the database."""
    form = SearchForm()

    
    
