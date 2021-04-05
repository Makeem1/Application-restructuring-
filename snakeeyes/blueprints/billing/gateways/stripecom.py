import stripe

class Plan(object):
    """Help to set plan"""
    @classmethod
    def retrieve(cls, plan):
        """Help to retrieve a plan if it exist"""

        try:
            return stripe.Plan.retrieve(plan)
        except stripe.error.StripeError as e:
            print(e)

    
    @classmethod
    def create(cls, id=None, name=None, amount=None, currency=None, interval=None, interval_count=None,
    trial_period_days=None, statement_descriptor = None, metadata=None):
        """Create a new stripe plan"""
        try:
            return stripe.Plan.create(
                id=id,
                name=name,
                amount=amount,
                currency=currency,
                interval=interval,
                interval_count=interval_count,
                trial_period_days=trial_period_days,
                statement_descriptor=statement_descriptor,
                metadata=metadata
            )
        except stripe.error.StripeError as e:
            print(e)

    
    @classmethod
    def update(cls, id=None, name=None, metadata=None, statement_descriptor=None):
        """Update an existing plan"""
        try:
            plan = stripe.Plan.retrieve(id)

            plan.name = name 
            plan.metadata = metadata
            plan.statement_descriptor = statement_descriptor
            return plan.save()
        except stripe.error.StripeError as e:
            print(e)


    @classmethod
    def delete(cls, plan):
        """Delete an existing plan"""
        try:
            plan = stripe.Plan.retrieve(plan)
            return plan.delete()
        except stripe.error.StripeError as e:
            print(e)

    
    @classmethod
    def list(cls):
        """List all available plan"""
        try:
            return stripe.Plan.all()
        except stripe.error.StripeError as e:
            print(e)


class Subscription(object):
    # User subscription class
    @classmethod
    def create(cls, token=None, email=None, coupon=None, plan=None):
        """
        Creating a user subscription for any plan user choose.

        All parameter are string and the the function return s customer subscription object
        """

        params = {
            'source':token,
            'email' : email,
            'plan' : plan
        }

        if coupon:
            param['coupon'] = coupon

        return stripe.Customer.create(**params)

    @classmethod
    def update(cls, customer_id=None, coupon=None, plan=None):
        """
        Updating a subscription plan for a user,m all param are string and it return stripe subscription.
        """

        customer = stripe.Customer.retrieve(customer_id)
        subscription_id = customer.subscriptions.data[0].id
        subscription = customer.subscriptions.retrieve(subscription_id)

        subscription.plan = plan 

        return subscription.save()

    @classmethod 
    def cancel(cls, customer_id=None):
        """This func cancel existing user subscription plan and the customer_id is the payment_id and return """

        customer = stripe.Customer.retrieve(customer_id)
        subscription_id = customer.subscriptions.data[0].id

        return customer.subscriptions.retrieve(subscription_id).delete()


class Invoice(object):
    @classmethod
    def upcoming(cls, customer_id):
        '''Retrieve an upcoming invoice for a user and return stripe invoice'''

        return stripe.Invoice.upcoming(customer=customer_id)


class Card(object):
    @classmethod
    def update(cls, customer_id, stripe_token=None):
        """Updating a user payment card and saving it to the database"""

        customer = stripe.Customer.retrieve(customer_id)
        customer.source = stripe_token 

        return customer.save()


class Coupon(object):
    @classmethod
    def create(cls, code=None, duration=None, amount_off=None, percent_off=None, currency=None, duration_in_months=None, max_redemptions=None, redeem_by=None):
        return stripe.Coupon.create(id=code,
                                    duration=duration,
                                    amount_off=amount_off,
                                    percent_off=percent_off,
                                    currency=currency,
                                    duration_in_months=duration_in_months,
                                    max_redemptions=max_redemptions,
                                    redeem_by=redeem_by
        )

    @classmethod
    def delete(cls, id=None):
        """Delete an existing coupon code"""
        coupon = stripe.Coupon.retrieve(id)
        return coupon.delete()

    @classmethod
    def update(cls, coupon_id=None):
        pass


class Event(object):
    @classmethod
    def retrieve(cls, even_id):
        """This is used to retrieve an even in order to protect us from malicious events not sent by stripe"""

        return stripe.Event.retrieve(even_id)





















    
