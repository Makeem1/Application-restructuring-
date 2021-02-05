from flask_mail import Message
from flask import current_app, render_template
from threading import Thread

from snakeeyes.extensions import mail

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(email, to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=email, recipients=[app.config['FLASKY_MAIL_SENDER']])
    msg.body = render_template(template + '.txt', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr



