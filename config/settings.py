DEBUG = True

SERVER_NAME = 'localhost.localdomain:8000'

SECRET_KEY = 'hellowrodjkadyggcwffkuwhneuedxkewhig'

# Email Configuration settings
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = '587'
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'patrickpwilliamson9@gmail.com'  # This email is not correct and will be overwritten by instance file
MAIL_PASSWORD = 'Olayinka1'  # This password is not and will be overwritten by instance settings file
MAIL_DEFAULT_SENDER = 'patrickpwilliamson9@gmail.com'

# Celery configuration 
CELERY_BROKER_URL = "redis://:olayinka@redis:6379/0"   #broker , password:olayinka and host:redis port:6379 database for redis : 0 
CELERY_RESULT_BACKEND = "redis://:olayinka@redis:6379/0" #backend, password:olayinka and host:redis port:6379 database for redis : 0 
CELERY_ACCEPT_CONTENT = ['json'] # accept only json data
CELERY_TASK_SERIALIZER = 'json' # serialize json data
CELERY_RESULT_SERIALIZER = 'json' # give the result as json data
CELERY_REDIS_MAX_CONNECTIONS = 5  # 













