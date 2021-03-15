from flask import render_template, request, current_app, url_for
from snakeeyes.admin import admin
from flask_login import login_required
from snakeeyes.admin.decorators import role_required
from snakeeyes.admin.models import DashBoard
from snakeeyes.admin.forms import SearchForm, UserForm
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
    form_search = SearchForm()

    page = request.args.get('page', 1, type =int )

    sort_by = User.sort_by(request.args.get('sort', 'created_on'), 
                                            request.args.get('direction', 'desc'))
    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    paginated_users = User.query \
        .filter(User.search(request.args.get('q', ''))) \
        .order_by(User.role.asc(), text(order_values)) \
        .paginate( page = page , per_page =current_app.config['FLASKY_POSTS_PER_PAGE'] , error_out = False )

    return render_template('admin/user/index.html', form = form_search , users = paginated_users )


@admin.route('users/edit/<int:id>', methods=['GET', 'POST'])
def users_edit(id):
    user = request.args.get(id) 
    form = UserForm(obj=user)

    if form.validate_on_submit():
        if user.is_last_admin(User, request.args.get('role'), request.args.get('active')):
            flash("You are the last admin, you can't perform the operation.", 'error')
            return redirect(url_for('admin.users'))

        user.username = form.username.data
        user.email = form.email.data
        user.active = form.active.data
        user.role = form.role.data
    
        if not user.username:
            user.username = None
        
        db.session.commit()

        if user.username:
            flash(f"{user.username} has been saved successfully", 'success')
        else:
            flash('User has been saved successfully', 'success')
            return redirect(url_for('admin.users'))
    
    form.username.data = user.username
    form.email.data = user.email
    form.active.data = user.active
    form.role.data = user.role


    return render_template('admin/user/edit.html', form = form , user = user )


