from snakeeyes.blueprints.billing.gateways.stripecom import Plan as PaymentPlan

from snakeeyes.extensions import db 
from snakeeyes import create_app

app = create_app()
db.app = app

def create_plan():
    """
    Sync a new plan 
    """

    if app.config['STRIPE_PLANS'] is None:
        return None

    for _, value in app.config['STRIPE_PLANS'].items():
        plan = PaymentPlan.retrieve(value.get('id'))

        if plan:
            PaymentPlan.update(
                id=value.get('id'),
                name = value.get('name'),
                metadata = value.get('metadata'),
                statement_descriptor = value.get('statement_descriptor')
            )

        else:
            PaymentPlan.create(**value)

    return None

def delete_plan(plans=None):
    """
    Delete plan or plans 
    : param plan : plan name
    : type : str

    :return : none

    """
    del_plan =[]
    if plans:
        del_plan.append(plans)
        for plan in del_plan:
            PaymentPlan.delete(plan)

    return None

    


def list_plan():
    """List all the plans"""

    return PaymentPlan.list()

