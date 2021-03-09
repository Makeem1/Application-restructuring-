from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Optional, Length


class SearchForm(Form):
    search = db.Column(db.StringField, validators=[Optional(), Length(min=4, max=128)])
    