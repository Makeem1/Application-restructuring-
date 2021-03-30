import datetime 
from snakeeyes.extensions import db

class Subscription(db.Model):
    __tablename__ ='subscriptions'

    id = db.Column(db.Integer, primary_key=True)

    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), index=True, nullable=False)

    plan = db.Column(db.String(128))
    coupon = db.Column(db.String(128))

    def __init__(self, **kwargs):
        super(Subscription,self).__init__(**kwargs)
        