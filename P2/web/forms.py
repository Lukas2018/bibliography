from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from config import Config


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('Pole wymagane')])
    password = PasswordField('Password', validators=[DataRequired('Pole wymagane')])
    submit = SubmitField('Sign In')
    user = Config.user

    def validate_username(self, username):
        if not self.user.check_user(username.data):
            raise ValidationError('Brak takiego użytkownika')

    def validate_password(self, password):
        if not self.user.validate_password(self.username.data, password.data):
            raise ValidationError('Niezgodne hasło')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired('Pole wymagane'), Length(min=3, max=30)])
    password = PasswordField('Password', validators=[DataRequired('Pole wymagane'), Length(min=8)])
    password_repeat = PasswordField('Repeat Password', validators=[DataRequired('Pole wymagane'), EqualTo('password'), Length(min=8)])
    submit = SubmitField('Sign Up')
    user = Config.user

    def validate_username(self, username):
        if self.user.check_user(username.data):
            raise ValidationError('Wybrany użytkownik już istnieje')