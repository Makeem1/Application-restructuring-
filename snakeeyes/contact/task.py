from snakeeyes import create_celery_app

from email import send_email


celery = create_celery_app()


celery.task
send_email()