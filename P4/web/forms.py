from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired, Length


class BibliographyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired('Pole wymagane'), Length(min=3, max=30)])
    author = StringField('Author', validators=[DataRequired('Pole wymagane'), Length(min=3, max=30)])
    date = DateField('Date', format='%Y-%m-%d')
    submit = SubmitField('Add Bibliography')
