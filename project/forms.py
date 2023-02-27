from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, SelectField, SearchField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, InputRequired, Optional
from project.models import Admin, User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = Admin.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')


class SearchForm(FlaskForm):
    type = SelectField('Filter', choices=[(1, 'username'), (2, 'email')])
    input = SearchField()

    submit = SubmitField('Find')


class AddUserForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    email = EmailField('Email', validators=[Optional()])
    phone = StringField('Phone', validators=[Optional()])
    comment = StringField('Comment')

    submit = SubmitField('Save')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

    def validate_phone(self, phone):
        user = User.query.filter_by(phone=phone.data).first()
        if user is not None:
            raise ValidationError('Current phone already exists')
