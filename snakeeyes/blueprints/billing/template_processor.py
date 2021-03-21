import datetime
import pytz

from lib.money import cent_to_dollar


def format_currency(amount, convert_to_dollars):
    '''format currency to 2 deciaml places'''

    if convert_to_dollars:
        amount = cent_to_dollar
    
    return "{:.2f}".format(amount)


def current_year():
    """return the current year"""

    return datetime.datetime.now(pytz.utc).year