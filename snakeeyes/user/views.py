from flask import flash, request, url_for, render_template, redirect
from snakeeyes.user.forms import LoginForm, RegisterForm
from snakeeyes.user import user
from flask_login import login_user, logout_user, login_required, logout_user
from snakeeyes.user.user_utils import safe_url


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            flash("You're now logged in.", 'succcess')
            if login_user(user, remember=form.remember_me.data) and user.is_active():
                user.track_user_activities(request.remote_addr)
                next_page = request.args.get('next')
                if next_page:
                    return redirect(url_for(safe_url(next_page)))
                else:
                    return redirect(url_for('user.settings'))
            else:
                flash("Your account has been temporary disable, please visit support for assisstance", 'info')
        elif user is None:
            flash("You need to register in order to access this page", 'info')
        else:
            flash('Incorrect password or email.', 'danger')
    return render_template('user/login.html', form=form)


@user.route('/logout')
@login_required
def logout():
    logout_user(user)
    return redirect(url_for('user.login'))


@user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created, you can now login with your email and password', 'success')
        return redirect(url_for('user.login'))
    return render_template('user/regsiter.html', form = form )


@user.route('/settings')
def settings():
    pass






    
    