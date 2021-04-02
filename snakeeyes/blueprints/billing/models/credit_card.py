import datetime

from lib.datetime_difference import  timedelta_days
from snakeeyes.extensions import db 

class CreditCard(db.Model):
    IS_EXPIRING_THRESHOLD_MONTHS = 60 

    __tablename__ = 'credit_cards'

    id = db.Column(db.Integer, primary_key=True)

    # Foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), index=True, nullable=False)

    # Card details
    brand = db.Column(db.String(32))
    last_4 = db.Column(db.Integer)
    exp_date = db.Column(db.Date, index=True)
    is_expiring = db.Column(db.Boolean(), nullable=False, server_default='0')

    def __init__(self, **kwargs):
        super(CreditCard, self).__init__(**kwargs)

    @classmethod
    def is_expiring_soon(cls, compare_date=None, exp_date=None):
        """Check card to expire in 60 days"""
        return exp_date <= timedelta_days(cls.IS_EXPIRING_THRESHOLD_MONTHS, compare_date=compare_date)

    @classmethod
    def mark_old_credit_card(cls, compare_date=None):
        """Mark credit card that are going to expire in two months or has expired"""

        today_with_delta = timedelta_days(cls.IS_EXPIRING_THRESHOLD_MONTHS, compare_date=compare_date)

        CreditCard.query.filter(cls.exp_date <= today_with_delta).update({cls.is_expiring:true})

        return db.session.commit()

    @classmethod
    def extract_card_params(cls, customer):
        """
        Extract the credit card info from paying customer 
        """
        card_data = customer.sources.data[0]
        exp_date = datetime.date(card_data.exp_year, card_data.exp_month, 1)

        card = {
            'brand' : card_data.brand,
            'last4' : card_data.last4,
            'exp_date' : exp_date,
            'is_expiring' : cls.is_expiring_soon(exp_date=exp_date)
        }

        return card 





    