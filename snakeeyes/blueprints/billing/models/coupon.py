import datetime
import string
from collections import OrderedDict
from random import choice

import pytz
from sqlalchemy import or_ , and_

from sqlalchemy.ext.hybrid import hybrid_property
from lib.money import cent_to_dollar, dollars_to_cents
from snakeeyes.extensions import db 
from snakeeyes.blueprints.billing.gateways.stripecom import Coupon as PaymentCoupon

class Coupon(db.Model):
    DURATION = [(
        ('forever', 'Forever'),
        ('once', 'Once'),
        ('repeating', 'Repeating')
    )]

    __tablename__ = 'coupons'

    id = db.Column(db.Integer, primary_key=True)

    # Coupon details
    code = db.Column(db.String(123), index=True, unique=True)
    duration = db.Column(db.Enum(*DURATION, name='duration_type'), index=True, nullable=False, server_default='forever')
    amount_off = db.Column(db.Integer())
    percent_off = db.Column(db.Integer())
    currency = db.Column(db.String(8))
    duration_in_months = db.Column(db.Integer())
    max_redemptions = db.Column(db.Integer(), index=True)
    redeem_by = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    times_redeemed = db.Column(db.Integer(), index=True, nullable=False, default=0)

    valid = db.Column(db.Boolean(), nullable=False, server_default='1')


    def __init__(self, **kwargs):
        if self.code:
            self.code = code.upper()
        else:
            self.code = Coupon.random_coupon_code()

        super(Coupon, self).__init__(**kwargs)


    @hybrid_property
    def redeemable(self):
        """
        Returns coupon code that are still valid. 
        """

        is_redeemable = or_(self.redeem_by.is_(None), self.redeem_by >= datetime.datetime.now)

        return and_(self.valid, is_redeemable)

    @classmethod
    def search(cls, query):
        """
        search resources by one or more filed
        """

        if not query:
            return ''

        search_query = '%{0}%'.format(query)

        return or_(cls.code.ilike(search_query))


    @classmethod
    def random_coupon_code(cls):
        """
        Create a human readable random code.
        """

        charset = string.digits + string.ascii_uppercase
        charset = charset.replace('B', '').replace('I', '')
        charset = charset.replace('O', '').replace('S', '')
        charset = charset.replace('0', '').replace('1', '')

        random_chars = ''.join(choice(charset) for _ in range(0, 14))

        coupon_code = '{}-{}-{}'.format(random_chars[0:4],
                                      random_chars[5:9],
                                      random_chars[10:14])

        return coupon_code


    @classmethod
    def expire_old_coupons(cls, compare_date=None):
        """
        Invalidate coupon that has pass thier expire date
        """

        if compare_date is None:
            compare_date = datetime.datetime.now(pytz.utc)

        cls.query.filter(cls.redeem_by <+ compare_date).update({cls.valid : not cls.valid})

        return db.session.commit()


    @classmethod
    def create(cls, params):
        """
        Create a coupon code and return true is successful
        """

        payment_params = params 

        payment_params['code'] = payment_params['code'].upper()

        if payment_params.get('amount_off'):
            payment_params['amount_off'] = dollars_to_cents(payment_params['amount_off'])

        PaymentCoupon.create(**payment_params)

        if 'id' in payment_params:
            payment_params['code'] = payment_params['id']
            del payment_params['id']

        if 'redeem_by' in payment_params:
            if payment_params.get('redeem_by') is not None:
                params['redeem_by'] = payment_params.get('redeem_by').replace(datetime.datetime.utcnow)

        coupon = Coupon(**payment_params)

        db.session.add(coupon)
        db.session.commit()

        return True









