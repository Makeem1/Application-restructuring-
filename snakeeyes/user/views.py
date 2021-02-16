from flask import flash, request, url_for, render_template, redirect
from snakeeyes.user.forms import LoginForm, RegisterForm, WelcomeForm, RequestPasswordResetForm, NewPasswordForm
from snakeeyes.user import user
from flask_login import login_user, logout_user, login_required, logout_user, current_user
from snakeeyes.user.user_utils import safe_url
from snakeeyes.user.decorator import anonymous_required
from snakeeyes.email import send_mail


@user.route('/login', methods=['GET', 'POST'])
@anonymous_required
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
                    return redirect(url_for('page.home'))
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
@anonymous_required
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_token()
        send_mail(user, 'contact', 'user/mail/index', token=token )
        flash('Your account has been created, you can now login with your email and password', 'success')
        return redirect(url_for('user.login'))
    return render_template('user/register.html', form = form )


@user.route('/confirm/<token>')
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('page.home'))
    if current_user.verify_token(token):
        flash("Your account has been confirmed", 'success')
        return redirect(url_for('page.home'))
    else:
        flash('Invalid link confirmation or expires link ', 'info')
    return redirect(url_for('user.unconfirmed'))

@user.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed and request.endpoint[:5] != 'user.':
        return redirect(url_for('user.unconfirmed'))

@user.before_app_request
def after_access_page():
    if current_user.is_authenticated and not current_user.username and request.endpoint[:5] != 'page.':
        flash("Choose a username to continue our services.", 'success')
        return redirect(url_for('user.welcome'))

@user.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('page.home'))
    return render_template('user/unconfirmed.html')


@user.route('/resend_link')
@login_required
def resend_link():
    token = current_user.generate_token()
    send_mail(current_user.email, 'contact', 'user/mail/index', token=token )
    flash("A new new email with a confirmation has been sent to your email.", 'success')
    return redirect(url_for('page.home'))


@user.route('/welcome', methods=['GET', 'POST'])
@login_required
def welcome():
    if current_user.username:
        return redirect(url_for('user.settings'))
    form = WelcomeForm()
    if form.validate_on_submit():
        current_user.username = form.username.data 
        db.session.commit()
        flash("Sign up is complete, you can now enjoy our serveices. Thank you.")
        return redirect(url_for('user.settins'))
    return render_template('user/welcome.html', form=form)


@user.route('/requestpasswordreset', methods=['GET', 'POST'])
@anonymous_required
def requestpasswordreset():
    form = RequestPasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        token = user.generate_token()
        send_mail(user, 'contact', 'user/mail/index', token=token )
        flash('Password reset link had been sent to your email', 'success')
        return redirect(url_for('user.login'))
    return render_template('user/requestpasswordreset.html', form = form)


@user.route('/settings')
@login_required
def settings():
    return render_template('user/settings.html')


@user.route('/account/newpassword/<token>', methods=['GET', 'POST'])
@anonymous_required
def newpassword(token):

    
    




















    
    