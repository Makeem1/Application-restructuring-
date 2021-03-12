from flask import render_template, request
from snakeeyes.admin import admin
from flask_login import login_required
from snakeeyes.admin.decorators import role_required
from snakeeyes.admin.models import DashBoard
from snakeeyes.admin.forms import SearchForm
from sqlalchemy import text
from snakeeyes.user.models import User



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

    page = request.args.get('page', 1, type =int )

    sort_by = User.sort_by(request.args.get('sort', 'created_on'), 
                                            request.args.get('direction', 'desc'))

    order_value = '{0} {1}'.format(sort_by[0], sort_by[1])

    paginated_users = User.query.filter(User.search(request.args.get('q', ''))).order_by(User.role.asc(), text(order_value)).paginate(page, 50, False)

    return render_template('admin/user/index.html', form = form , users = paginated_users )
    
