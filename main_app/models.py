from main_app import db, login_manager, app
from datetime import datetime, timedelta
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
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(6), nullable=False)
    password = db.Column(db.String, nullable=False)
    personal_data = db.relationship('User_personalData', back_populates='user', uselist=False)
    personal_loan = db.relationship("Loan", back_populates="loan_user", uselist=False)
    account = db.relationship('Account', back_populates='user', uselist=False)
    withdrawals = db.relationship('Withdrawals', back_populates='user', uselist=False)
    deposits = db.relationship('Deposit', back_populates='user', uselist=False)
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


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=True)  # Nullable for bank account
    user = db.relationship('User', back_populates='account')
    created_at = db.Column(db.DateTime, default=datetime.now())
    balance = db.Column(db.Float, default=0.0)  # Holds the account balance
    account_type = db.Column(db.String(50), default='User')  # Could be 'User' or 'Bank'   


    def deposit(self, amount):
        """Deposit an amount into the account."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        
        self.balance += amount  # Update the balance
        db.session.commit()  # Save the changes to the database

    def __repr__(self):
        return f'<Account {self.id}, Type: {self.account_type}, Balance: {self.balance}>'


class Deposit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship('User', back_populates='deposits')
    amount = db.Column(db.Float, nullable=False)
    deposit_method = db.Column(db.String(50), nullable=False)
    reference_no = db.Column(db.String(50), nullable=False, unique=True)
    account_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    

    def __repr__(self):
        return f'<Deposit {self.id}, Amount: {self.amount}, Method: {self.deposit_method}>'


class Withdrawals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship('User', back_populates='withdrawals')
    amount = db.Column(db.Float, nullable=False)
    withdrawal_method = db.Column(db.String(50), nullable=False)
    account_type = db.Column(db.String(50), nullable=False)
    transaction_fee = db.Column(db.Float, nullable=False)
    total_deducted = db.Column(db.Float, nullable=False)
    reference_no = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(10), db.ForeignKey('user.user_id'), nullable=False)
    loan_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    rejection_reason = db.Column(db.String(120), nullable=True)
    loan_term = db.Column(db.Integer, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)  # Annual interest rate
    total_amount_due = db.Column(db.Float, nullable=False, default=0.0)  # Amount after interest
    monthly_payment = db.Column(db.Float, nullable=False, default=0.0)  # Payment With interest
    purpose = db.Column(db.String(120), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    next_due_date = db.Column(db.DateTime, nullable=False)
    amount_paid = db.Column(db.Float, default=0)
    penalty = db.Column(db.Float, nullable=False, default=0.0)  # Add a penalty field
    loan_user = db.relationship('User', back_populates='personal_loan', lazy=True, uselist=False)
    disbursement = db.relationship('Disbursement', back_populates='loan', lazy=True, uselist=False)
    repayment = db.relationship('Repayment', back_populates='loan', lazy=True, uselist=False)

    def set_initial_due_date(self):
        self.next_due_date = self.start_date + timedelta(days=30)  # First due date is 30 days after the loan is issued

    @property
    def rounded_total_amount_due(self):
        return round(self.total_amount_due, 2)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship('User', back_populates='transactions')
    transaction_type = db.Column(db.String(50))  # 'deposit', 'repayment', 'withdraw', 'disbursement'
    amount = db.Column(db.Float, nullable=False)
    method = db.Column(db.String(50), nullable=False)
    account_type = db.Column(db.String(50), nullable=False)
    transaction_date = db.Column(db.DateTime, default=datetime.now())
    reference_no = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Float, nullable=False)


class Disbursement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loan.id'))
    loan = db.relationship('Loan', back_populates='disbursement')
    source_account = db.Column(db.String(50))  # Source of funds (e.g., bank account)
    disbursed_amount = db.Column(db.Float)
    disbursement_date = db.Column(db.DateTime, default=datetime.now())


class Repayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loan.id'))
    loan = db.relationship('Loan', back_populates='repayment')
    amount_paid = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.now())
    destination_account = db.Column(db.String(50))