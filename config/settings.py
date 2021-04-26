from datetime import timedelta
import os

DEBUG = True
LOG_LEVEL = 'DEBUG'

# Google analytics 
ANALYTICS_GOOGLE_UA = 'foo'


basedir = os.path.abspath(os.path.dirname(__file__))


SERVER_NAME = '127.0.0.1:5000'

SECRET_KEY = 'hellowrodjkadyggcwffkuwhneuedxkewhig'
WTF_CSRF_ENABLED = False

# Email Configuration settings
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = '587'
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'patrickpwilliamson9@gmail.com'  # This email is not correct and will be overwritten by instance file
MAIL_PASSWORD = 'Olayinka1'  # This password is not and will be overwritten by instance settings file
MAIL_DEFAULT_SENDER = 'patrickpwilliamson9@gmail.com'
FLASKY_MAIL_SUBJECT_PREFIX = 'Snake Eyes user'
FLASKY_MAIL_SENDER = 'patrickpwilliamson9@gmail.com'

# Celery configuration 
CELERY_BROKER_URL = "redis://:olayinka@redis:6379/0"   #broker , password:olayinka and host:redis port:6379 database for redis : 0 
CELERY_RESULT_BACKEND = "redis://:olayinka@redis:6379/0" #backend, password:olayinka and host:redis port:6379 database for redis : 0 
CELERY_ACCEPT_CONTENT = ['json'] # accept only json data
CELERY_TASK_SERIALIZER = 'json' # serialize json data
CELERY_RESULT_SERIALIZER = 'json' # give the result as json data
CELERY_REDIS_MAX_CONNECTIONS = 5  # 



db_uri = 'postgresql://postgres:Olayinka1?@localhost:5432/snakeeyes' 
# SQLALCHEMY_DATABASE_URI='sqlite:///site.db'
SQLALCHEMY_DATABASE_URI=db_uri
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
FLASKY_POSTS_PER_PAGE = 50 


# User 
SEED_ADMIN_EMAIL = 'dev@local.host'
SEED_ADMIN_PASSWORD = 'devpassword'
REMEMBER_COOKIE_DURATION = timedelta(days=90)


# Stripe Api
# Billing.
STRIPE_SECRET_KEY = 'sk_test_51IWV8MKKBISTKSZXn8bVHDuSPzMpkBooewRaVVQqKBfty8ebRygkBGl0iZMkePtEBUJLJKwqJotnQws0MRqNkGUX00ikA2m2P8'
STRIPE_PUBLISHABLE_KEY = 'pk_test_51IWV8MKKBISTKSZXNSODH7mvRhj5uPkIHoFU1fPrtOXkLVWez5Fwy526Qb6ximsdxxfij9b0JYHmn44bhHyZrt2200zVMOhRm7'
STRIPE_API_VERSION = '2016-03-07'
STRIPE_PLANS = {
    '0': {
        'id': 'bronze',
        'name': 'Bronze',
        'amount': 100,
        'currency': 'usd',
        'interval': 'month',
        'interval_count': 1,
        'trial_period_days': 14,
        'statement_descriptor': 'SNAKEEYES BRONZE',
        'metadata': {
            'coins' : 120
        }
    },
    '1': {
        'id': 'gold',
        'name': 'Gold',
        'amount': 500,
        'currency': 'usd',
        'interval': 'month',
        'interval_count': 1,
        'trial_period_days': 14,
        'statement_descriptor': 'SNAKEEYES GOLD',
        'metadata': {
            'coins' : 600,
            'recommended': True
        }
    },
    '2': {
        'id': 'platinum',
        'name': 'Platinum',
        'amount': 1000,
        'currency': 'usd',
        'interval': 'month',
        'interval_count': 1,
        'trial_period_days': 14,
        'statement_descriptor': 'SNAKEEYES PLATINUM',
        'metadata': {
            'coins' : 1500
        }
    }
}


# Bet.
DICE_ROLL_PAYOUT = {
    '2': 36.0, 
    '3': 18.0,
    '4': 12.0,
    '5': 9.0,
    '6': 7.2,
    '7': 6.0,
    '8': 7.2,
    '9': 9.0,
    '10': 12.0,
    '11': 18.0,
    '12': 36.0
}

# RATELIMIT_STORAGE_URL = CELERY_BROKER_URL
# RATELIMIT_STRATEGY = 'fixed-window-elastic-expiry'
# RATELIMIT_HEADERS_ENABLED = True










