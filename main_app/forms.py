""" Form Classes
"""
from flask_wtf import FlaskForm
from wtforms import (StringField, EmailField, PasswordField, IntegerField,
                     TelField, DateField, SubmitField, RadioField)
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from main_app.models import User
from flas_login import current_user



class ApplicationForm(FlaskForm):
    """ Registration Form"""
    surname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=25)])
    other_names = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    dob = DateField('Date of Birth', validators=[DataRequired()])
    id_number = IntegerField('ID Number', validators=[DataRequired()])
    phone_number = TelField('Phone Number', validators=[DataRequired(), Length(min=10)])
    address = StringField('Address', validators=[DataRequired(), Length(min=2, max=30)])
    postal_code = IntegerField('Postal Code', validators=[DataRequired()])
    passport_photo = FileField('Passport Photo', validators=[FileAllowed(['jpg, jpeg'])])
    copy_photo = FileField('Copy of ID Card/Passport', validators=[FileAllowed(['jpg, jpeg'])])
    gender = RadioField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    submit = SubmitField('Save Info')
    

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already taken. Please choose a different one.")
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already taken. Please choose a different one.")    

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ResetPasswordRequestForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')

        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("There is no account with that email. You must register first.")  

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    user_profile = FileField('Copy of ID Card/Passport', validators=[FileAllowed(['jpg, jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username already exists. Please choose a different one.")
            

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Confirm')