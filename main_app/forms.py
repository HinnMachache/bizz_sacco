""" Form Classes
"""
from flask_wtf import FlaskForm
from wtforms import (StringField, EmailField, PasswordField, IntegerField,
                     TelField, DateField, SubmitField, RadioField, HiddenField,
                     SelectField)
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from main_app.models import User, Admin



class ApplicationForm(FlaskForm):
    """ Registration Form"""
    email = SelectField("Email", validators=[DataRequired()])
    surname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=25)])
    other_names = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    dob = DateField('Date of Birth', validators=[DataRequired()])
    id_number = IntegerField('ID Number', validators=[DataRequired()])
    phone_number = TelField('Phone Number', validators=[DataRequired(), Length(min=10)])
    address = StringField('Address', validators=[DataRequired(), Length(min=2, max=30)])
    postal_code = IntegerField('Postal Code', validators=[DataRequired()])
    passport_photo = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    copy_photo = FileField('Copy of ID Card/Passport', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    gender = RadioField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    submit = SubmitField('Save Info')
    

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = HiddenField('Role', default='user')  # To determine Privileges
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
        admin = Admin.query.filter_by(email=email.data).first()
        if user is None and admin is None:
            raise ValidationError("There is no account with that email. You must register first.")  

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Confirm')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    user_profile = FileField('Profile Picture:', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Update Profile')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username already exists. Please choose a different one.")
            

class UpdateAdminForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=30)])
    submit = SubmitField('Update Profile')

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
