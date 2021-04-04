from flask import Blueprint, request, redirect, url_for, render_template, flash, current_app, render_template
from flask_login import current_user, login_required
from config import settings
from snakeeyes.blueprints.billing.decorators import subscription_required, handle_stripe_exceptions
from snakeeyes.blueprints.billing.models.subscriptions import Subscription 
from snakeeyes.blueprints.billing.forms import CreditCardForm, UpdateSubscriptionForm, CancelSubscriptionForm
from config import settings

billing = Blueprint('billing', __name__, template_folder='../templates', url_prefix='/billing')


@billing.route('/pricing')
def pricing():
    if current_user.is_authenticated and current_user.subscription:
        return redirect(url_for('billing.update'))

    form = UpdateSubscriptionForm()

    return render_template('billing/pricing.html', form=form,
                           plans=settings.STRIPE_PLANS)


@billing.route('/create', methods=['GET', 'POST'])
@handle_stripe_exceptions
@login_required
def create():
    if current_user.subscription:
        flash('You already have an active subscription.', 'info')
        return redirect(url_for('user.settings'))

    plan = request.args.get('plan')
    subscription_plan = Subscription.get_plan_by_id(plan)

    # Guard against an invalid or missing plan.
    if subscription_plan is None and request.method == 'GET':
        flash('Sorry, that plan did not exist.', 'error')
        return redirect(url_for('billing.pricing'))

    stripe_key = current_app.config.get('STRIPE_PUBLISHABLE_KEY')
    print(stripe_key)
    form = CreditCardForm(stripe_key=stripe_key, plan=plan)

    if form.validate_on_submit():
        subscription = Subscription()
        created = subscription.create(user=current_user,
                                      name=request.form.get('name'),
                                      plan=request.form.get('plan'),
                                      coupon=request.form.get('coupon_code'),
                                      token=request.form.get('stripe_token'))
        print(request.form.get('stripe_token'))
        if created:
            flash('Awesome, thanks for subscribing!', 'success')
        else:
            flash('You must enable JavaScript for this request.', 'warning')

        return redirect(url_for('user.settings'))

    return render_template('billing/payment_method.html',
                           form=form, plan=subscription_plan)


@billing.route('/update')
@subscription_required
@handle_stripe_exceptions
@login_required
def update():
    current_plan = current_user.subscription.plan
    activa_plan = Subscription.get_plan_by_id(current_plan)
    new_plan = Subscription.get_new_plan(request.form.keys())

    plan = Subscription.get_new_plan(new_plan)

    # Guard against invalid plan or similar plan 
    is_same_plan = new_plan == activa_plan['id']
    if ((new_plan is not None and plan is None) or is_same_plan) and request.method == 'POST':
        return redirect(url_for('billing.update'))

    form = UpdateSubscriptionForm(coupon = current_user.subscriptions.coupon)

    if form.validate_on_submit:
        subscription = Subscription()
        updated = subscription.update(user=current_user,
                                     coupon=form.coupon_code.data,
                                     plan=plan.get('id'))

        if updated:
            flash('Your plan has been updated.', 'success')
            return redirect(url_for('user.settings'))

    return render_template('billing/pricing.html', form = form , plans = settings.STRIPE_PLANS, active_plan = activa_plan)   


@billing.route('/cancel')
@handle_stripe_exceptions
@login_required
def cancel():
    if not current_user.subscription:
        flash('You do not have active subscription.', 'info')
        return redirect(url_for('billing.pricing'))

    form = CancelSubscriptionForm()

    if form.validate_on_submit:
        subscription = Subscription()
        cancelled = subscription.cancel(user = current_user)

        if cancelled:
            flash('Sorry to see you go, your subscription has been calcelled', 'success')
            return redirect(url_for('user.settings'))

    return render_template('billing/cancel.html', form = form)


@billing.route('/update')
@handle_stripe_exceptions
@login_required
def update_paymethod_method():
    if not current_user.credit_card:
        flash('You do not have a payment credit card on file.', 'info')
        return redirect(url_for('user.settings'))

    active_plan = Subscription.get_plan_by_id(current_user.subscripion.plan)

    card = current_user.credit_card
    stripe_key = current_app.config.get('STRIPE_PUBLISHABLE_KEY')
    form = CreditCardForm(stripe_key=stripe_key,
                          plan=active_plan,
                          name=current_user.name)

    if form.validate_on_submit:
        subscription = Subscription()
        updated = subscription.update(user = current_user,
                                      credit_card = card,
                                      name = request.form.get('name'),
                                      token = request.form.get('stripe_token'))

        if updated:
            flash('You payment method has been updated.', 'success')
        else:
            flash('You must enable javascript for this request.', 'warning')

        return redirect(url_for('user.settings'))
    return render_template('billing/payment_method.html', form=form, plan=active_plan, card_last4 = str(card.last4))
