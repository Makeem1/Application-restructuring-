import datetime
from snakeeyes.extensions import db 
from snakeeyes.blueprints.billing.gateways.stripecom import Invoice as PaymentInvoice

class Invoice(db.Model):
    __tablename__ = 'invoices' 

    # Unique ID
    id = db.Column(db.Integer, primary_key = True)

    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', onupdate = 'CASCADE', ondelete='CASCADE'), index=True, nullable=False)

    # Invoices details 
    plan = db.Column(db.String(128), index=True)
    receipt_number = db.Column(db.String(128), index=True)
    description = db.Column(db.String(128))
    period_start_on = db.Column(db.Date())
    period_end_on = db.Column(db.Date())
    currency = db.Column(db.String(12))
    tax = db.Column(db.Integer())
    tax_percent = db.Column(db.Float())
    total = db.Column(db.Integer())

    # De-normalize the card details so we can render a user's history properly even if they have no active subscription or change cards at some point 

    brand = db.Column(db.String(32))
    last4 = db.Column(db.Integer)
    exp_date = db.Column(db.Date, index=True)

    # Invoice runtime 
    created_on = db.Column(db.DateTime(), default = datetime.datetime.utcnow)

    def __init__(self, **kwargs):   
        super(Invoice, self).__init__(**kwargs)


    @classmethod
    def billing_history(cls, user=None):
        """
        Return a billing history for a particular user
        """
        invoices = cls.query.filter(cls.user_id == user.id).order_by(cls.created_on.desc()).limit(12)

        return invoices

    @classmethod
    def parse_from_api(cls, payload):
        """
        Parse and return invoice information we are interested in.
        """
        plan_info = payload['lines']['data'][0]['plan']
        date = datetime.datetime.utcfromtimestamp(payload['date'])

        invoice = {
            'plan': plan_info['name'],
            'description': plan_info['statement_descriptor'],
            'next_bill_on': date,
            'amount_due': payload['amount_due'],
            'interval': plan_info['interval']
        }

        return invoice


    @classmethod
    def upcoming(cls, customer_id):
        """
        Return the upcoming invoice
        """

        invoice = PaymentInvoice.upcoming(customer_id=customer_id)

        return Invoice.parse_from_api(invoice)


    
    
    







