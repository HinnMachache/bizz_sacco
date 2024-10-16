from main_app import db, login_manager, app
from datetime import datetime
import jwt
from time import time
from flask_login import UserMixin   # Manage sessions


@login_manager.user_loader
def load_user(user_id):
    user_id = str(user_id)
    if user_id.startswith('user_'):
        return User.query.get(user_id)
    elif user_id.startswith('admin_'):
        return Admin.query.get(user_id)
    return None  # Return None if no user/admin is found


class User(db.Model, UserMixin):
    user_id = db.Column(db.String(10), primary_key=True)
    personal_data = db.relationship('User_personalData', back_populates='user', uselist=False)
    personal_loan = db.relationship("Loan", back_populates="loan_user", uselist=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(6), nullable=False)
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
    user_id = db.Column(db.String, db.ForeignKey('user.user_id'), nullable=False)  # Foreign Key
    user = db.relationship('User', back_populates='personal_data', lazy=True)
    surname = db.Column(db.String(30), nullable=False)
    other_names = db.Column(db.String(120), nullable=False)
    income = db.Column(db.Float, nullable=False)
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
    admin_id = db.Column(db.String(10), primary_key=True)
    personal_data = db.relationship('Admin_personalData', back_populates='admin', uselist=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(6), nullable=False)
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
    admin_id = db.Column(db.String, db.ForeignKey('admin.admin_id'), nullable=False)  # Foreign Key
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
    
# Show newly registered users to admin
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    is_read = db.Column(db.Boolean, default=False)


# Show newly submitted Loan to admin
class LoanNotification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    is_processed = db.Column(db.Boolean, default=False)


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(10), db.ForeignKey('user.user_id'), nullable=False)
    loan_user = db.relationship('User', back_populates='personal_loan', lazy=True)
    loan_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    loan_term = db.Column(db.Integer, nullable=False)
    purpose = db.Column(db.String(120), nullable=False)
    transactions = db.relationship('Transaction', back_populates='loan')


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loan.id'), nullable=False)
    loan = db.relationship('Loan', back_populates='transactions')
    transaction_type = db.Column(db.String(50))  # 'disbursement' or 'repayment'
    amount = db.Column(db.Float)
    transaction_date = db.Column(db.DateTime, default=datetime.now())
    status = db.Column(db.String(50))

class Disbursement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loan.id'))
    source_account = db.Column(db.String(100))  # Source of funds (e.g., bank account)
    disbursed_amount = db.Column(db.Float)
    disbursement_date = db.Column(db.DateTime, default=datetime.utcnow)