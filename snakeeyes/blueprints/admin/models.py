from snakeeyes.extensions import db 
from snakeeyes.blueprints.user.models import User
from snakeeyes.blueprints.billing.models.subscriptions import Subscription
from snakeeyes.blueprints.bet.models.bet import Bet
from sqlalchemy import func 


class DashBoard(object):
    @classmethod
    def group_and_count_users(cls):
        """class method to count and group all user base on role"""
        return DashBoard._group_and_count(User, User.role)

    @classmethod
    def group_and_count_plans(cls):
        """
        Perform a group by and count on all subscribers
        """
        return DashBoard._group_and_count(Subscription, Subscription.plan)

    @classmethod
    def group_and_count_coupons(cls):
        '''
        Obtain coupon code statistic across subscribers 
        '''
        not_null = db.session.query(Subscription).filter(Subscription.coupon.isnot(None)).count()
        total = db.session.query(func.count(Subscription.id)).scalar()

        if total == 0:
            percent = 0 
        else:
            percent = round((not_null / float(total)), 1)
        return not_null, total, percent

    @classmethod
    def group_and_count_payouts(cls):
        """
        Grouping payouts 
        """

        return DashBoard._group_and_count(Bet, Bet.payout)

    @classmethod
    def _group_and_count(cls, model , field):
        """This is a private method to count and group a specific user"""

        count = func.count(field)
        query = db.session.query(count, field).group_by(field).all()

        result = {
            'query' : query , 
            'total' : model.query.count()
        }

        return result
