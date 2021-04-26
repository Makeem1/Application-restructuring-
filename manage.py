from snakeeyes import create_app
from flask_script import Manager, Shell
from snakeeyes.blueprints.user.models import User
from snakeeyes.extensions import db
from snakeeyes.blueprints.billing.models.coupon import Coupon
from snakeeyes.blueprints.billing.models.invoice import Invoice
from snakeeyes.blueprints.billing.models.subscriptions import Subscription
from snakeeyes.blueprints.billing.models.credit_card import CreditCard
from snakeeyes.blueprints.bet.models.bet import Bet

from stripe_utils import create_plan, delete_plan, list_plan

app = create_app()
manager = Manager(app)

db.app = app 

def make_shell_context():
    return dict(app=app, User=User, Coupon=Coupon, Invoice=Invoice, Subscription=Subscription, CreditCard=CreditCard, Bet=Bet, db=db, create_plan=create_plan, delete_plan=delete_plan, list_plan = list_plan )
manager.add_command('shell', Shell(make_context=make_shell_context))


if __name__ == '__main__':
    manager.run()


