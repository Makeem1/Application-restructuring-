from flask_wtf import Form
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Optional, Length


class SearchForm(Form):
    search = StringField('Search terms', validators=[Optional(), Length(min=4, max=128)])


# class BulkDeleteForm(Form):
#     list_activity = [('all_selected_items', 'All selected items'), ('all_search_results', 'All search results')]

#     scope = SelectField('Privileges',  )