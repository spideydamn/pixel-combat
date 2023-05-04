# -*- coding: cp1251 -*-

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, BooleanField, FileField
from wtforms.validators import DataRequired, Optional


class RegisterForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    password_again = PasswordField('repeat password', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    submit = SubmitField('SIGN UP')


class LoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember me')
    submit = SubmitField('SIGN IN')


class EditForm(FlaskForm):
    email = EmailField('email: ', validators=[DataRequired()])
    username = StringField('username: ', validators=[DataRequired()])
    old_password = PasswordField('old password: ', validators=[Optional()])
    password = PasswordField('new password: ', validators=[Optional()])
    password_again = PasswordField('repeat new password: ', validators=[Optional()])
    avatar = FileField('avatar: ', validators=[Optional()])
    submit = SubmitField('SAVE')