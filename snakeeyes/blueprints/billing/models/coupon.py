import datetime
import string
from collections import OrderedDict
from random import choice

import pytz
from sqlalchemy import or_ , and_

from sqlalchemy.ext.hybrid import hybrid_property
from lib.money import cent_to_dollars, dollars_to_cents
from snakeeyes.extensions import db 
from snakeeyes.blueprints.billing.gateways.stripecom import Coupon as PaymentCoupon


class Coupon(db.Model):
    DURATION = OrderedDict([
        ('once', 'Once'),
        ('repeating', 'Repeating'),
        ('forever', 'Forever')
    ])

    __tablename__ = 'coupons'
    id = db.Column(db.Integer, primary_key=True)

    # Coupon details.
    code = db.Column(db.String(128), index=True, unique=True)
    duration = db.Column(db.Enum(*DURATION, name='duration_types'),
                         index=True, nullable=False, default='forever')
    amount_off = db.Column(db.Integer())
    percent_off = db.Column(db.Integer())
    currency = db.Column(db.String(8))
    duration_in_months = db.Column(db.Integer())
    max_redemptions = db.Column(db.Integer(), index=True)
    redeem_by = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    times_redeemed = db.Column(db.Integer(), index=True,
                               nullable=False, default=0)
    valid = db.Column(db.Boolean(), nullable=False, server_default='1')

    created_on = db.Column(db.DateTime(), default=datetime.datetime.utcnow)

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

        # search_query = '%{0}%'.format(query)
        # search_chain = (User.email.ilike(search_query),
        #                 User.username.ilike(search_query))
                        
        # return or_(*search_chain)

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

        # Stripe will save the coupon to id field on stripe while on our database, we want it to save on code field
        if 'id' in payment_params:
            payment_params['code'] = payment_params['id']
            del payment_params['id']

        # Converting th eunix time to day stim stamp that is acceptable by the databse
        if 'redeem_by' in payment_params:
            if payment_params.get('redeem_by') is not None:
                params['redeem_by'] = payment_params.get('redeem_by').replace(datetime.datetime.utcnow)

        coupon = Coupon(**payment_params)

        db.session.add(coupon)
        db.session.commit()

        return True


    @classmethod
    def bulk_delete(cls, ids):
        """
        Override the general bulk delete method to delete coupon from application and stripe
        """
        delete_count = 0

        for id in ids:
            coupon = Coupon.query.get(id)
            print(coupon)

            if coupon is None:
                continue 
                
            # Delete on stripe 
            stripe_delete = PaymentCoupon.delete(coupon)

            # If successful, delete it locally 
            if stripe_delete.get('deleted'):
                db.session.delete(coupon)
                delete_count += 1

        return delete_count


    @classmethod
    def find_by_code(cls, code):
        """
        Find a coupon by its code 
        """

        formatted_code = code.upper()

        coupon = Coupon.query.filter(Coupon.redeemable, Coupon.code == formatted_code).first()

        return coupon 


    def redeem(self):
        """
        Update redeem stats for this coupon
        """
        self.times_redeemed += 1

        if self.max_redemptions:
            if self.times_redeemed >= self.max_redemptions:
                self.valid = False

        return db.session.commit()


    def to_json(self):
        """
        Retun JSON fields to represent a coupon 
        """

        params = {
            'duration' : self.duration,
            'duration_in_months' : self.duration_in_months
        }


        if self.amount_off:
            params['amount_off'] = cent_to_dollar(self.amount_off)

        if self.percent_off:
            params['percent_off'] = self.percent_off

        return params

    @classmethod
    def sort_by(cls, field, direction):
        """This help to sort the user base on the field column and direction. """

        if field not in cls.__table__.columns:
            field = "created_on"
        
        if direction not in ('asc', 'desc'):
            direction = 'asc'

        return field, direction


    @classmethod
    def get_bulk_action_ids(cls, scope, ids, omit_ids=[], query=''):
        """Determine which id to be deleted."""
        omit_ids = list(map(str, omit_ids))


        if scope == 'all_search_result':
            ids = cls.query.with_entities(cls.id).filter(cls.search(query))
            
            ids = [ str(item[0]) for item in ids]


        if omit_ids:
            ids = [id for id in ids if id not in omit_ids]

        return ids