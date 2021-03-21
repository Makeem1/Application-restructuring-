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















    
