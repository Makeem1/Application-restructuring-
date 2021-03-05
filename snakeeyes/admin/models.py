from snakeeyes.extensions import db 
from snakeeyes.user.models import User
from sqlalchemy import func 


class DashBoard(object):
    @classmethod
    def group_and_count_users(cls):
        """class method to count and group all user base on role"""
        return DashBoard._group_and_count_users(User, User.role)

    @classmethod
    def _group_and_count_users(cls, model , field):
        """This is a private method to count and group a specific user"""

        count = func.count(field)
        query = db.session.query(count, field).group_by(field).all()

        result = {
            'query' : query , 
            'total' : model.query.count()
        }

        return result
