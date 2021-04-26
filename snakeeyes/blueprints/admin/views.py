from flask import render_template, request, current_app, url_for, flash, redirect
from snakeeyes.blueprints.admin import admin
from flask_login import login_required
from snakeeyes.blueprints.admin.decorators import role_required
from snakeeyes.blueprints.admin.models import DashBoard
from snakeeyes.blueprints.admin.forms import SearchForm, UserForm, BulkDeleteForm , CanUserSubscriptionForm, CouponForm
from sqlalchemy import text
from snakeeyes.blueprints.user.models import User
from flask_login import current_user
from snakeeyes.extensions import db 
from snakeeyes.blueprints.billing.models.subscriptions import Subscription
from snakeeyes.blueprints.billing.decorators import handle_stripe_exceptions

from snakeeyes.blueprints.billing.models.coupon import Coupon


@admin.before_request
@login_required
@role_required('admin')
def before_request():
    """Function to monitor admin page"""
    pass


@admin.route('')
def dashboard():
    group_and_count_users = DashBoard.group_and_count_users()
    group_and_count_plans = DashBoard.group_and_count_plans()
    group_and_count_coupons = DashBoard.group_and_count_coupons()
    group_and_count_payouts = DashBoard.group_and_count_payouts()
    return render_template('admin/page/admin.html', group_and_count_users = group_and_count_users, 
                            group_and_count_coupons = group_and_count_coupons,
                            group_and_count_plans = group_and_count_plans, 
                            group_and_count_payouts=group_and_count_payouts)


@admin.route('/users')
def users():
    """Fucntion to list all users in the database."""
    form_search = SearchForm()
    bulk_form = BulkDeleteForm()
    sort_by = User.sort_by(request.args.get('sort', 'created_on'), 
                                            request.args.get('direction', 'desc'))
    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    page = request.args.get('page', 1 , type=int)
    paginated_users = User.query \
        .filter(User.search(request.args.get('q', ''))) \
        .order_by(User.role.asc(), text(order_values)) \
        .paginate( page = page , per_page =current_app.config['FLASKY_POSTS_PER_PAGE'] , error_out = False )

    return render_template('admin/user/index.html', form=form_search,
                                users=paginated_users, bulk_form=bulk_form)


@admin.route('users/edit/<int:id>', methods=['GET', 'POST'])
def users_edit(id):
    user = User.query.get(id)
    form = UserForm()

    if form.validate_on_submit():
        if user.is_last_admin(user, form.role.data, form.active.data):
            flash("You are the last admin, you can't perform the operation.", 'error')
            return redirect(url_for('admin.users'))

        user.username = form.username.data
        user.active = form.active.data
        user.role = form.role.data
    
        if not user.username:
            user.username = None
        
        db.session.commit()

        if user.username:
            flash(f"{user.username} has been saved successfully", 'success')
            return redirect(url_for('admin.users'))
        else:
            flash('User has been saved successfully', 'success')
            return redirect(url_for('admin.users'))
    
    form.username.data = user.username
    form.active.data = user.active
    form.role.data = user.role
    db.session.commit()

    return render_template('admin/user/edit.html', form=form , user=user )


@admin.route('/users/bulk_delete', methods=['POST'])
def users_bulk_delete():
    form = BulkDeleteForm()

    if form.validate_on_submit():
        ids = User.get_bulk_action_id(request.form.get('scope'),
                                       request.form.getlist('bulk_ids'),
                                       omit_id=[current_user.id],
                                       query=request.args.get('q', ''))

        delete_count = User.bulk_delete(ids)

        flash('{0} user(s) were scheduled to be deleted.'.format(delete_count),
              'success')
    else:
        flash('No users were deleted, something went wrong.', 'error')

    return redirect(url_for('admin.users'))


@admin.route('/canel_user_subscription')
def canel_user_subscription():
    form = CanUserSubscriptionForm()

    if form.validate_on_submit():
        user = User.query.get(request.form.get('id'))

        if user: 
            subscription = Subscription()
            if subscription.cancel(user):
                flash('Subscription has been cancelled for user {0}'.format(user.name), 'success')
            else:
                flash('No subscription was cancelled', 'success')

    return redirect(url_for('admin.users'))


# Coupon --------------------------------------------------------------------

@admin.route('/coupons', methods=['GET', 'POST'])
@handle_stripe_exceptions
def coupons():
    """Fucntion to list all users in the database."""
    form_search = SearchForm()
    bulk_form = BulkDeleteForm()
    sort_by = Coupon.sort_by(request.args.get('sort', 'created_on'), 
                                            request.args.get('direction', 'desc'))
    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    page = request.args.get('page', 1 , type=int)
    paginated_users = Coupon.query \
        .filter(Coupon.search(request.args.get('q', ''))) \
        .order_by(text(order_values)) \
        .paginate( page = page , per_page =current_app.config['FLASKY_POSTS_PER_PAGE'] , error_out = False )

    return render_template('admin/coupon/index.html', form=form_search,
                                coupons=paginated_users, bulk_form=bulk_form)

 
@admin.route('/coupons/new', methods=['GET', 'POST'])
@handle_stripe_exceptions
def coupons_new():
    coupon = Coupon()
    form = CouponForm(obj=coupon)

    if form.validate_on_submit():
        form.populate_obj(coupon)

        params = {
            'code': coupon.code,
            'duration': coupon.duration,
            'percent_off': coupon.percent_off,
            'amount_off': coupon.amount_off,
            'currency': coupon.currency,
            'redeem_by': coupon.redeem_by,
            'max_redemptions': coupon.max_redemptions,
            'duration_in_months': coupon.duration_in_months,
        }

        if Coupon.create(params):
            flash('Coupon has been created successfully.', 'success')
            return redirect(url_for('admin.coupon'))

    return render_template('admin/coupon/new.html', form=form, coupon=coupon)

@admin.route('/coupon/bulk_delete', methods=['POST'])
def coupon_bulk_delete():
    form = BulkDeleteForm()

    if form.validate_on_submit():
        ids = Coupon.get_bulk_action_ids(request.form.get('scope'),
                                        request.form.getlist('bulk_id'),
                                        query=request.args.get('q', ''))

        Coupon.bulk_delete(ids)

        flash('{0} coupon(s) will be deleted.'.format(len(ids)), 'succes')
    else:
        flash('No coupon were deleted, something went wrong', 'error')
    return redirect(url_for('admin.coupon'))