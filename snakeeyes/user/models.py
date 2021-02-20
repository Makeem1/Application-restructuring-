from snakeeyes.extensions import db
import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from snakeeyes.extensions import login_manager
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(24), nullable=True, unique=True)
    email = db.Column(db.String(128), nullable=False, unique = True)
    active = db.Column(db.Boolean, default = True, nullable=False)
    hash_password = db.Column(db.String(240), nullable=False)
    confirmed = db.Column(db.Boolean(), default = False, nullable=False)

    sign_in_count = db.Column(db.Integer, default=0)
    current_sign_in_on = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    current_sign_in_ip = db.Column(db.String(24)) 
    last_sign_in_on = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    last_sign_in_ip = db.Column(db.String(24)) 


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


    def track_user_activities(self, ip_address):
        self.sign_in_count = +1

        self.last_sign_in_on = self.current_sign_in_on
        self.last_sign_in_ip = self.current_sign_in_ip

        self.current_sign_in_ip = ip_address
        self.current_sign_in_on = datetime.datetime.utcnow

        return True

    
    def generate_token(self, expiration=3600):
        s = TimedJSONWebSignatureSerializer('current_app.config["SECRET_KEY"]', expires_in=expiration)
        return s.dumps({"user_id": self.id})


    def verify_token(self, token):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False

        if data.get('user_id') != self.id:
            self.confirmed = False
        self.confirmed = True
        db.session.commit()
        return User.query.get(data['user_id'])

    def create_table(self):
        db.drop_all()
        db.create_all()

        




        
        


        
