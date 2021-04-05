from flask import flash, request, url_for, render_template, redirect, current_app
from snakeeyes.blueprints.user.forms import LoginForm, RegisterForm, WelcomeForm, RequestPasswordResetForm, NewPasswordForm, UpdateAccountForm, PasswordField
from snakeeyes.blueprints.user import user
from flask_login import login_user, logout_user, login_required, current_user, confirm_login
from snakeeyes.blueprints.user.user_utils import safe_url
from snakeeyes.blueprints.user.models import User
from snakeeyes.email import send_mail
from snakeeyes.extensions import db


@user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_token()
        send_mail(user.email, 'contact', 'user/mail/index', customer=user ,token=token )
        flash('Your account has been created, you can now login with your email and password', 'success')
        return redirect(url_for('user.login'))
    return render_template('user/register.html', form = form )


@user.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("Operation already performed", 'info')
        return redirect(url_for('page.home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        current_app.logger.debug('{0} has tried to log in with ip : {1}'.format(form.email.data, request.remote_addr))

        if user is not None and user.verify_password(form.password.data):
            if login_user(user, remember=True) and user.is_active():
                flash('Log in successful', 'success')
                user.track_user_activities(request.remote_addr)
                next_page = request.args.get('next')
                if next_page:
                    return redirect(safe_url(next_page))
                else:
                    return redirect(url_for('page.home'))
            else:
                flash("Your account has been temporary disable, please visit support for assisstance", 'info')
                return redirect(url_for('user.login'))
        elif user is None:
            flash("You need to register in order to access this page", 'info')
        else:
            flash('Incorrect password or email.', 'danger')
    return render_template('user/login.html', form=form)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You are logged out", 'success')
    return redirect(url_for('user.login'))


@user.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('page.home'))
    if current_user.verify_token(token):
        flash("Your account has been verified", 'success')
    else:
        flash('The confirmation link has expired or invalid', 'danger')
    return redirect(url_for('page.home'))


@user.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.confirmed and request.endpoint[:5] != 'user.':
        return redirect(url_for('user.unconfirmed'))


@user.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('page.home'))
    return render_template('user/unconfirmed.html')


@user.route('/resend_link')
@login_required
def resend_link():
    token = current_user.generate_token()
    send_mail(current_user.email, 'contact', 'user/mail/unconfirmed', user = current_user, token=token )
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
        return redirect(url_for('user.settings'))
    return render_template('user/welcome.html', form=form)


@user.route('/updateaccount', methods=['GET', 'POST'])
@login_required
def update_credentials():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        new_password = form.password.data
        new_email = form.email.data
        if new_password:
            current_user.password = new_password
            flash('Your password has been updated', 'success')
        elif new_email:
            current_user.email = new_email
            db.session.commit()
            flash('Your email has been updated', 'success')
            send_mail(current_user.email, 'contact', 'user/mail/index', token=token )
        else:
            flash("Your credentials has been updated", 'Thanks')
    return render_template('user/updatecredentials.html', form = form)


@user.route('/settings')
@login_required
def settings():
    return render_template('user/settings.html')


@user.route('/requestpasswordreset', methods=['GET', 'POST'])
def requestpasswordreset():
    if current_user.is_authenticated:
        flash("Operation already performed", 'info')
        return redirect(url_for('page.home'))
    form = RequestPasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_mail(user.email, 'reset password token', 'user/mail/reset_password', user = user, token=token )
            flash('Password reset link had been sent to your email', 'success')
            return redirect(url_for('user.login'))
        else:
            flash('Unable to find your account', 'warning')
            return redirect(url_for('user.requestpasswordreset'))
    return render_template('user/requestpasswordreset.html', form = form)


@user.route('/new_password/<token>', methods=['GET', 'POST'])
def newpassword(token):
    if current_user.is_authenticated:
        flash("Operation already performed", 'info')
        return redirect(url_for('page.home'))
      
    form = NewPasswordForm()
    if form.validate_on_submit():
        user = User.confirm_reset_token(token)
        if user is None:
            flash('Your reset token has expired or invalid', 'danger')
            return redirect(url_for('user.requestpasswordreset'))

        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        flash('Your password has been reset successfully.', 'success')
        return redirect(url_for('user.login'))
    return render_template('user/newpassword.html', form=form)



    


    
    




















    
    