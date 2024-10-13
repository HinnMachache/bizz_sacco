from main_app import db, login_manager, app
import jwt
from time import time
from flask_login import UserMixin   # Manage sessions


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    if user is None:
        return Admin.query.get(int(user_id))
    return user

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    personal_data = db.relationship('User_personalData', back_populates='user', uselist=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    # personal_data_submitted = db.Column(db.Boolean, default=False)

    def to_dict(self):
            return {
                'user_id': self.user_id,
                'username': self.username,
                'email': self.email,

            }

    def get_id(self):
        return self.user_id
    
    def get_reset_password_token(self, expires_in=1800):
        return jwt.encode({
            'reset_password': self.user_id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256'
        )
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            usr_id = jwt.decode(token, app.config['SECRET_KEY'],
                                algorithms=['HS256'])['reset_password']
        except:
            return None
        return User.query.get(usr_id)

    def __repr__(self) -> str:
        return f"User -> {self.username} : {self.email}"


class User_personalData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)  # Foreign Key
    user = db.relationship('User', back_populates='personal_data', lazy=True)
    surname = db.Column(db.String(30), unique=True, nullable=False)
    other_names = db.Column(db.String(120), unique=True, nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    id_number = db.Column(db.Integer, unique=True, nullable=False)
    telephone_no = db.Column(db.String(20), unique=True, nullable=False)
    address = db.Column(db.String(50), nullable=False)
    postal_code= db.Column(db.Integer, nullable=False)
    gender= db.Column(db.String(5), nullable=False)
    user_profile = db.Column(db.String(20), nullable=False, default="user.jpeg")
    id_profile = db.Column(db.String(20), nullable=False, default="user.jpeg")


    def __repr__(self) -> str:
        return f"User Data -> {self.surname} : {self.other_names} : {self.user_profile}"
    

class Admin(db.Model, UserMixin):
    admin_id = db.Column(db.Integer, primary_key=True)
    personal_data = db.relationship('Admin_personalData', back_populates='admin', uselist=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    # personal_data_submitted = db.Column(db.Boolean, default=False)

    def to_dict(self):
            return {
                'admin_id': self.admin_id,
                'username': self.username,
                'email': self.email,
                # add any other fields you need
            }

    def get_id(self):
        return self.admin_id
    
    def get_reset_password_token(self, expires_in=1800):
        return jwt.encode({
            'reset_password': self.admin_id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256'
        )
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            usr_id = jwt.decode(token, app.config['SECRET_KEY'],
                                algorithms=['HS256'])['reset_password']
        except:
            return None
        return Admin.query.get(usr_id)

    def __repr__(self) -> str:
        return f"{self.username} : {self.email}"


class Admin_personalData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.admin_id'), nullable=False)  # Foreign Key
    admin = db.relationship('Admin', back_populates='personal_data', lazy=True)
    surname = db.Column(db.String(30), unique=True, nullable=False)
    other_names = db.Column(db.String(120), unique=True, nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    id_number = db.Column(db.Integer, unique=True, nullable=False)
    telephone_no = db.Column(db.String(20), unique=True, nullable=False)
    address = db.Column(db.String(50), nullable=False)
    postal_code= db.Column(db.Integer, nullable=False)
    gender= db.Column(db.String(5), nullable=False)
    user_profile = db.Column(db.String(20), nullable=False, default="user.jpeg")
    id_profile = db.Column(db.String(20), nullable=False, default="user.jpeg")


    def __repr__(self) -> str:
        return f"Admin Data -> {self.surname} : {self.other_names} : {self.user_profile}"