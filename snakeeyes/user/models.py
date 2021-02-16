from snakeeyes.extensions import db
import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from snakeeyes.extensions import login_manager
from flask import current_app



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(24), nullable=False, unique=True, server_default='')
    email = db.Column(db.String(128), nullable=False, unique = True, server_default='')
    active = db.Column(db.Boolean(), server_default = '1', nullable=False)
    hash_password = db.Column(db.String(128), nullable=False)
    confirmed = db.Column(db.Boolean(), server_default='False', nullable=False)

    count_sign_in = db.Column(db.Integer(), default = 0)
    current_sign_in_on = db.Column(db.DateTime(), default=datetime.datetime.utcnow, nullable=False)
    current_sign_in_ip = db.Column(db.String(24), nullable = False) 
    last_sign_in_on = db.Column(db.DateTime(), default=datetime.datetime.utcnow, nullable=False)
    last_sign_in_ip = db.Column(db.String(24), nullable = False) 


    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')


    @password.setter
    def password(self, password):
        self.hash_password = generate_password_hash(password)


    def verify_password(self, password):
        return check_password_hash(self.hash_password, password)


    def is_active(self):
        return self.active()


    def track_user_activities(self, ip_address):
        self.count_sign_in = +1

        self.last_sign_in_on = self.current_sign_in_on
        self.last_sign_in_ip = self.current_sign_in_ip

        self.current_sign_in_ip = ip_address
        self.current_sign_in_on = datetime.datetime.utcnow

        return True

    
    def generate_token(self, expiration=3600):
        secret_key = current_app.config['SECRET_KEY']
        s = JSONWebSignatureSerializer("secret-key", expires_in= expiration)
        return s.dumps({"user_id": self.id})

    def verify_token(self, token):
        s = JSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False

        if data.get('user_id') != self.email:
            self.confirmed = False
        self.confirmed = True
        db.session.commit()
        return True

    def create_table():
        db.drop_all()
        db.create_all()

        




        
        


        
