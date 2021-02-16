from snakeeyes.extensions import db
import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from snakeeyes.extensions import login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(24), nullable=False, unique=True, server_default='')
    email = db.Column(db.String(128), nullable=False, unique = True, server_default='')
    active = db.Column(db.Boolean(), server_default = '1', nullable=True)
    hash_password = db.Column(db.String(128), nullable=False)

    count_sign_in = db.Column(db.Integer(), default = 0)
    current_sign_in_on = db.Column(db.DateTime(), default=datetime.datetime.utc, nullable=False)
    current_sign_in_ip = db.Column(db.String(24), nullable = False) 
    last_sign_in_on = db.Column(db.DateTime(), default=datetime.datetime.utc, nullable=False)
    last_sign_in_ip = db.Column(db.String(24), nullable = False) 

    @property
    def password(self):
        raise AttributeError("The passowrd is a read only attribute.")


    @password.setter
    def passowrd(self, password):
        return self.hash_password = generate_password_hash(password)
        

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