from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length, EqualTo

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=100)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')
