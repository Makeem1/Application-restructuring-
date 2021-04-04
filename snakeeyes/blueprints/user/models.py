from snakeeyes.extensions import db
import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from snakeeyes.extensions import login_manager
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer
from collections import OrderedDict
from sqlalchemy import or_
from faker import Faker as fake
from snakeeyes.blueprints.billing.models.credit_card import CreditCard
from snakeeyes.blueprints.billing.models.subscriptions import Subscription
from snakeeyes.blueprints.billing.models.invoice import Invoice

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    ROLE = OrderedDict([
        ('member', "Member"),
        ("admin", "Admin")
    ])
    
    # Unique idntification number
    id = db.Column(db.Integer, primary_key = True)

    # Credit card relationship 
    credit_card = db.relationship(CreditCard, uselist=False, backref='users', passive_deletes=True)

    # Subscription relationship
    subscription = db.relationship(Subscription, backref='users', uselist=False, passive_deletes=True)

    # Invoic Relationships 
    invoice = db.relationship(Invoice, backref='users', passive_deletes=True)

    # User credentials
    role = db.Column(db.Enum(*ROLE, name = 'role_type', native_enum = False), nullable = False, default='member')
    username = db.Column(db.String(128), nullable=True, unique=True)
    email = db.Column(db.String(128), nullable=False, unique = True)
    active = db.Column(db.Boolean, default = True, nullable=False)
    hash_password = db.Column(db.String(240), nullable=False)
    confirmed = db.Column(db.Boolean, default = False)

    # User tracking information 
    sign_in_count = db.Column(db.Integer, default=0)
    current_sign_in_on = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    current_sign_in_ip = db.Column(db.String(24)) 
    last_sign_in_on = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    last_sign_in_ip = db.Column(db.String(24)) 

    # Billing.
    name = db.Column(db.String(128), index=True)
    payment_id = db.Column(db.String(128), index=True)
    cancelled_subscription_on = db.Column(db.DateTime(), default=datetime.datetime.utcnow)

    # User run time
    created_on = db.Column(db.DateTime(), default = datetime.datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)



    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')


    @password.setter
    def password(self, password):
        self.hash_password = generate_password_hash(password)


    def verify_password(self, password):
        return check_password_hash(self.hash_password, password)


    def is_active(self):
        return self.active


    @classmethod
    def search(cls, query):
        """
        Search a resource by 1 or more fields.

        :param query: Search query
        :type query: str
        :return: SQLAlchemy filter
        """
        if not query:
            return ''

        search_query = '%{0}%'.format(query)
        search_chain = (User.email.ilike(search_query),
                        User.username.ilike(search_query))
                        
        return or_(*search_chain)

    @classmethod
    def sort_by(cls, field, direction):
        """This help to sort the user base on the field column and direction. """

        if field not in cls.__table__.columns:
            field = "created_on"
        
        if direction not in ('asc', 'desc'):
            direction = 'asc'

        return field, direction

    
    @classmethod
    def is_last_admin(cls, user, new_role, new_active):
        """This particular method will help to check if this particular user is the last admin."""

        is_changing_role = user.role == 'admin' and new_role != 'admin'
        is_changing_active = user.active is True and new_role is None

        if is_changing_role or is_changing_active :
            admin_count = User.query.filter(User.role == 'admin').count()
            active_count = User.query.filter(User.is_active is True).count()

            if admin_count == 1 or active_count == 1:
                return True
                
        return False


    @classmethod
    def get_bulk_action_id(cls, scope, ids, omit_id=None, query=''):
        """Determine bulk of id to be deleted."""
        omit_id = list(map(str, omit_id))

        if scope == 'all_search_result':
            ids = User.query.with_entities(User.id).filter(User.search(query))

            ids = [str(item[0]) for item in ids]

        if omit_id:
            ids = [id for id in ids if id not in omit_id]

        return ids

    @classmethod
    def bulk_delete(cls, ids):
        """Delete selected user id"""

        delete_count = User.query.filter(User.id.in_(ids)).delete(synchronize_session=False)

        return delete_count


    def track_user_activities(self, ip_address):
        self.sign_in_count = +1

        self.last_sign_in_on = self.current_sign_in_on
        self.last_sign_in_ip = self.current_sign_in_ip

        self.current_sign_in_ip = ip_address
        self.current_sign_in_on = datetime.datetime.utcnow()

        return True

    
    def generate_token(self, expiration=3600):
        s = TimedJSONWebSignatureSerializer(current_app.config["SECRET_KEY"],  expires_in=expiration)
        return s.dumps({"confirm": self.id}).decode('utf-8')


    def verify_token(self,token):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False

        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        user = User.query.filter_by(id = data.get('confirm')).first()
        return user.email


    def generate_reset_token(self):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def confirm_reset_token(token):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False

        user = User.query.get(data.get('user_id'))

        return user.id


    @classmethod
    def add_fake(cls):
        from random import seed, randint, choice
        from sqlalchemy.exc import IntegrityError
        from snakeeyes.extensions import fake

        users = []

        seed()
        while len(users) < 100:
            u = User(
                email = fake.email(),
                username = fake.name()+str(randint(0, 300)),
                active = bool(choice([True, False])),
                password = 'password',
                sign_in_count = randint(0,20),
                current_sign_in_on = fake.date_time_between(start_date='-1y', end_date='now'),
                last_sign_in_ip = fake.ipv4(),
                confirmed = bool(choice([True, False])),
                current_sign_in_ip = fake.ipv4(),
                last_sign_in_on = fake.date_time_between(start_date='-1y', end_date='now'),
                created_on = fake.date_time_between(start_date='-15y', end_date='now'),
                updated_on = fake.date_time_between(start_date='-15y', end_date='now')
            )

            users.append(u)

            db.session.add(u)

            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

            


        




        
        


        
