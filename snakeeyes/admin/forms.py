from flask_wtf import Form
from wtforms import StringField, SelectField, ValidationError, BooleanField, SelectField
from wtforms.validators import DataRequired, Optional, Length
from snakeeyes.user.models import User


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
    username = StringField('Username', validators=[Optional(), Length(min=4, max=28)])
    role = SelectField('Priviledegs', validators=[DataRequired()], choices = Role )
    active = BooleanField("Check to allow user to sign in.")

    def validate_username(self, username):
        user = User.query.filter_by(username = user.usemane ).first()

        if user :
            raise ValidationError("Username already taken by another user, please choose another username. Thanks")
