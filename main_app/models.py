from main_app import db, login_manager, app
import jwt
from time import time
from flask_login import UserMixin   # Manage sessions


@login_manager.user_loader  # Reloading the user from user id stored in the session
def load_user(user_id):
    return User.query.get(int(user_id))

class BaseUser(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    # personal_data_submitted = db.Column(db.Boolean, default=False)

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
        return f"{self.username} : {self.email}"

class User(BaseUser):
    user_id = db.Column(db.Integer, db.ForeignKey('base_user.user_id'), primary_key=True)
    personal_data = db.relationship('User_personalData', back_populates='user', uselist=False)
   
    def __repr__(self) -> str:
        return f"User: {self.username} : {self.email}"
    

class Admin(BaseUser):
    user_id = db.Column(db.Integer, db.ForeignKey('base_user.user_id'), primary_key=True)
    personal_data = db.relationship('Admin_personalData', back_populates='user', uselist=False)
   
    def __repr__(self) -> str:
        return f"Admin: {self.username} : {self.email}"
    

class BaseUser_personalData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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
        return f"{self.surname} : {self.other_names} : {self.user_profile}"

class User_personalData(BaseUser_personalData):
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), index=True)  # Foreign Key
    user = db.relationship('User', back_populates='personal_data', lazy=True)
    

    def __repr__(self) -> str:
        return f"User: {self.surname} : {self.other_names} : {self.user_profile}"


class Admin_personalData(BaseUser_personalData):
    user_id = db.Column(db.Integer, db.ForeignKey('admin.user_id'), index=True)  # Foreign Key
    user = db.relationship('User', back_populates='personal_data', lazy=True)
    

    def __repr__(self) -> str:
        return f"Admin: {self.surname} : {self.other_names} : {self.user_profile}"