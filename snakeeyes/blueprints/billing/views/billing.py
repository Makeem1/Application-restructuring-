from flask import Blueprint, request, redirect, url_for, render_template, flash, current_app, render_template
from flask_login import current_user, login_required
from config import settings
from snakeeyes.blueprints.billing.decorators import subscription_required, handle_stripe_exceptions
from snakeeyes.blueprints.billing.models.subscriptions import Subscription 
from snakeeyes.blueprints.billing.forms import CreditCardForm, UpdateSubscriptionForm
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
        return redirect(url_for("user.settings"))

    plan = request.args.get('plan')
    
    subscription_plan = Subscription.get_plan_by_id(plan)

    if subscription_plan is None and request.method=='GET':
        flash('Sorry, the plan did not exist.', 'error')
        return redirect(url_for('billing.pricing'))

    stripe_key = current_app.config.get('STRIPE_PUBLISHABLE_KEY')
    print(stripe_key)
    form = CreditCardForm(stripe_key=stripe_key, plan=plan)

    if form.validate_on_submit:
        subscription = Subscription()
        created = subscription.create(user=current_user,
                                      name=form.name.data,
                                      plan=form.plan.data,
                                      coupon=form.coupon_code.data,
                                      token=request.form.get('stripe_token'))
        if created:
            flash('Awesome, thanks for subscribing!', 'success')
        else:
            flash('You must enable javascript in your browser', 'info')

        return redirect(url_for('user.settings'))

    return render_template('billing/payment_method.html',
                           form=form, plan=subscription_plan)





    
        






    

