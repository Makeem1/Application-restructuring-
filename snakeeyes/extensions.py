from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail 
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager
from faker import Faker
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


debug_toolbar = DebugToolbarExtension()
mail = Mail()
Csrf = CSRFProtect()
db = SQLAlchemy()
login_manager = LoginManager()
fake = Faker()
limiter = Limiter(key_func=get_remote_address)

