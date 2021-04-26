from flask_wtf import Form
from wtforms import (
    StringField, 
    SelectField,
    ValidationError, 
    BooleanField, 
    SelectField, 
    IntegerField,
    FloatField, 
    DateTimeField
    )

from wtforms.validators import (
    DataRequired, 
    Optional, 
    Length,
    NumberRange
    )

from snakeeyes.blueprints.user.models import User
from lib.locale import Currency
from lib.utils_wtform import choices_from_dict
from snakeeyes.blueprints.billing.models.coupon import Coupon


class SearchForm(Form):
    search = StringField('Search terms', validators=[Optional(), Length(min=4, max=128)])


class BulkDeleteForm(Form):
    SCOPE = [
        ('all_selected_items', 'All selected items'),
        ('all_search_results', 'All search results')
    ]

    scope = SelectField('Priviledges', validators=[DataRequired()], choices= SCOPE)


class UserForm(Form):
    Role = [('member', "Member"),
        ("admin", "Admin")]

    coins = IntegerField('Coins', validators=[DataRequired(), 
                        NumberRange(min=1, max=21345678)])
    username = StringField('Username', validators=[Optional(), Length(min=4, max=28)])
    role = SelectField('Priviledegs', validators=[DataRequired()], choices = Role )
    active = BooleanField("Check to allow user to sign in.")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data ).first()

        if user :
            raise ValidationError("Username already taken by another user, please choose another username. Thanks")


class CanUserSubscriptionForm(Form):
    pass


class CouponForm(Form):
    percent_off = IntegerField('Percent of (%)',
                                validators=[Optional(), NumberRange(min=1, max=100)])
    amount_off = FloatField('Amount off ($)', 
                                validators=[Optional(), NumberRange(min=0.01, max=21474836.0)])
    
    code = StringField('Code', 
                            validators=[DataRequired(), Length(min=1, max=32)])
    
    currency = SelectField('Currency', validators=[DataRequired()], 
                            choices=choices_from_dict(Currency.TYPES, prepend_blank=False))
    
    duration = SelectField('Duaration', 
                            validators=[DataRequired()], 
                            choices=choices_from_dict(Coupon.DURATION, prepend_blank=False))
    
    duration_in_months = IntegerField('Duration', 
                        validators=[Optional(), NumberRange(min=1, max=12) ])
    
    max_redemptions = IntegerField('Max Redeemptions', 
                                    validators=[Optional(), NumberRange(min=1, max=2147483647)])
    
    redeem_by = DateTimeField('Redeem by', 
                                validators=[Optional()], format='%Y-%m-%d %H:%M:%S')

    def validate(self):
        if not Form.validate(self):
            return False

        result = True

        percent_off = self.percent_off.data
        amount_off = self.amount_off.data

        if percent_off is None and amount_off is None:
            empty_error = 'Pick atleast one.'
            self.percent_off.errors.append(empty_error)
            self.amount_off.errors.append(empty_error)
            result = False
        elif percent_off and amount_off:
            both_error = 'Cannot pick both'
            self.percent_off.errors.append(both_error)
            self.amount_off.errors.append(both_error)

            return False
        else:
            pass


        return result


