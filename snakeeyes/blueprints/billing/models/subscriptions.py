import datetime 
from snakeeyes.extensions import db
from snakeeyes.blueprints.billing.models.credit_card import CreditCard 
from snakeeyes.blueprints.billing.models.coupon import Coupon
from snakeeyes.blueprints.billing.gateways.stripecom import Card as PaymentCard
from snakeeyes.blueprints.billing.gateways.stripecom import Subscription as PaymentSubscription
from config import settings


class Subscription(db.Model):
    __tablename__ ='subscriptions'

    id = db.Column(db.Integer, primary_key=True)

    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), index=True, nullable=False)

    plan = db.Column(db.String(128))

    coupon = db.Column(db.String(128))

    def __init__(self, **kwargs):
        super(Subscription,self).__init__(**kwargs)


    @classmethod
    def get_plan_by_id(cls, plan):
        """Identify plan by id and compare"""

        for key, value in settings.STRIPE_PLANS.items():
            if value.get('id') == plan:
                return settings.STRIPE_PLANS[plan]
            
        return None

    @classmethod
    def get_new_plan(cls, keys):
        """Pick plan based on the plan identifier"""

        for key in keys:
            split_key = key.split('submit_')

            if isinstance(split_key, list) and len(split_key)== 2:
                if Subscription.get_plan_by_id(split_key[1]):
                    return split_key[1]
      return None


    def create(cls, user=None, plan=None, coupon=None, token=None, name=None ):
        """Create a recurring subscription"""

        if token is None:
            return False

        if coupon:
            self.coupon = coupon.upper()

        customer = PaymentSubscription.create(token=token,
        email=user.email,coupon=coupon=, plan=plan)

        # Updating user details 
        user.name = name 
        user.payment_id = customer.id
        user.cancelled_subscription_on = None

        # Set the subscription details
        self.user_id = user.id
        self.plan = plan

        # Redeem the coupon
        if coupon:
            coupon=Coupon.query.filter(Coupon.coupon == self.coupon).first()
            coupon.redeem()

        db.session.add(user)
        db.session.add(self)

        db.session.commit()

        return True

    def update(self, user=None, plan=None, coupon=None):
        """Updating an existing subscription plan"""

        PaymentSubscription.update(customer_id=user.payment_id, coupon=coupon, plan =plan)

        user.subscribtion.plan = plan 
        if coupon:
            user.subscription.coupon = coupon
            coupon = Coupon.query.filter(Coupon.coupon == coupon).first()

            if coupon:
                coupon.redeem()

        db.session.add(user.subscription)
        db.session.commit()

        return True 


    def cancel(self, user=None, discard_credit_card=None):
        """Cancel an existing subscription"""

        PaymentSubscription.cancel(user.payment_id)
        user.payment_id = None
        user.cancelled_subscription_on = datetime.datetime.now(pytz.utc)

        db.session.add(user)
        db.session.delete(user.subscription)

        if discard_credit_card:
            db.session.delete(user.credit_card)

        db.session.commit()

        return True


    def update_paymethod_method(self, user=None, credit_card=None, name=None, token=None):
        """Updating user existing user card"""

        if token is None:
            return False

        customer = PaymentSubscription.update(customer_id=user.payment_id, token=token)

        # Update user details 
        user.name = name

        # Update the credit card 
        new_card = CreditCard.extract_card_params(customer)
        credit_card.brand = new_card.get('brand')
        credit_card.last4 = new_card.get('last4')
        credit_card.exp_date = new_card.get('exp_date')
        credit_card.is_expiring = new_card.get('is_expiring')

        db.session.add(user)
        db.session.add(credit_card)

        db.session.commit()

        return True


