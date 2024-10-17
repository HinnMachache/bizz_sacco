import secrets
import os
import logging
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from functools import wraps
from PIL import Image
from main_app import app, db, bcrypt, mail
from flask import render_template, flash, request, url_for, redirect, current_app, abort
from main_app.models import (User, User_personalData, Admin, Admin_personalData, Notification,
                             LoanNotification, Loan, Disbursement, Transaction, Repayment, Account,
                             Withdrawals, Deposit)
from main_app.forms import (RegistrationForm, LoginForm, ApplicationForm,
                            ResetPasswordRequestForm, ResetPasswordForm,
                            ChangePasswordForm, UpdateAccountForm, AdminRegistrationForm, LoanForm)
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message
from main_app import db
from main_app.models import User, Admin, Loan



# Role Required Decorator
def role_required(role):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login'))
            try:
                if current_user.role != role:
                    flash("You do not have permission to access this page.")
                    abort(404, description="You do not have permission to access this page.")
                    return redirect(url_for('home'))                  
            except AttributeError:
                abort(404, description="You do not have permission to access this page. Access denied. Please contact Admin")
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


def promote_user_to_admin(user_id):
    user = User.query.filter_by(user_id=user_id).first()

    if user:
        existing_admin = Admin.query.filter_by(email=user.email).first()
        if existing_admin:
            return False  # User is already an admin

        # Promote the user to admin
        new_admin = Admin(
            username=user.username,
            email=user.email,
            password=user.password
        )
        

        db.session.add(new_admin)
        db.session.delete(user)
        db.session.commit()
        return True
    else:
        return False

# Set up logging configuration
logging.basicConfig(filename='app.log', level=logging.DEBUG,  # Set the logging level to DEBUG
                format='%(asctime)s - %(levelname)s - %(message)s') 

# Add User data to database
@app.route("/admin/personal_data", methods=["POST", "GET"])
@role_required("admin")
@login_required
def add_personal_data():
    form=ApplicationForm()

    users = User.query.all()  # Fetch all users
    admins = Admin.query.all() # Fetch all admins
    form.email.choices = [(user.email, user.email) for user in users ] + [(admin.email, admin.email) for admin in admins] 

    
    if form.validate_on_submit():
        user_email = form.email.data
        user = User.query.filter_by(email=user_email).first()
        admin = Admin.query.filter_by(email=user_email).first()

        if user:
            p_data = User_personalData(user_id=user.user_id, surname=form.surname.data, other_names=form.other_names.data, dob=form.dob.data,
                                id_number=form.id_number.data, telephone_no=form.phone_number.data, address=form.address.data,
                                postal_code=form.postal_code.data, gender=form.gender.data, income=form.income.data)

            # Save passport photo
            if form.passport_photo.data:
                passport_photo_file = save_picture(form.passport_photo.data)
                p_data.user_profile = passport_photo_file
            
            # Save copy of ID card/passport
            if form.copy_photo.data:
                copy_photo_file = save_identification(form.copy_photo.data)
                p_data.id_profile = copy_photo_file

            try:
                db.session.add(p_data)
                db.session.commit()
                flash("Personal data added successfully!", 'success')

                return redirect(url_for('admin_index'))
            except Exception as e:
                print("Error occured durin commit")
                db.session.rollback()  # Rollback in case of error
                print(f"Error committing data: {e}")
                flash("An error occurred while saving personal data.", 'error')
            except IntegrityError as e:
                flash("IntegrityError occurred during commit")

                db.session.rollback()  # Rollback in case of error
                flash("An error occurred: Duplicate surname or telephone number entry. Please check these fields.", 'error')
                # Check for which field caused the integrity error
            
                flash("An error occurred while saving personal data.", 'error')
        elif admin:
            admin_data = Admin_personalData(admin_id=admin.admin_id, surname=form.surname.data, other_names=form.other_names.data, dob=form.dob.data,
                                id_number=form.id_number.data, telephone_no=form.phone_number.data, address=form.address.data,
                                postal_code=form.postal_code.data, gender=form.gender.data)

            # Save passport photo
            if form.passport_photo.data:
                passport_photo_file = save_picture(form.passport_photo.data)
                admin_data.user_profile = passport_photo_file
            
            # Save copy of ID card/passport
            if form.copy_photo.data:
                copy_photo_file = save_identification(form.copy_photo.data)
                admin_data.id_profile = copy_photo_file

            try:
                db.session.add(admin_data)
                db.session.commit()
                flash("Personal data added successfully!", 'success')

                return redirect(url_for('admin_index'))
            except Exception as e:
                print("Error occured durin commit")
                db.session.rollback()  # Rollback in case of error
                print(f"Error committing data: {e}")
                flash("An error occurred while saving personal data.", 'error')
            except IntegrityError as e:
                flash("IntegrityError occurred during commit")

                db.session.rollback()  # Rollback in case of error
                flash("An error occurred: Duplicate surname or telephone number entry. Please check these fields.", 'error')
                # Check for which field caused the integrity error
            
                flash("An error occurred while saving personal data.", 'error')
        else:
            flash("User not found."), 404

    elif request.method == 'GET':
        if form.email.data:  # Check if there is a selected email
            main_mail = form.email.data  # Get the selected email
            print(f"Selected email: {main_mail}")  # Debug log

            user = User.query.filter_by(email=main_mail).first()
            admin = Admin.query.filter_by(email=main_mail).first()
        else:
            print("No email selected")
        
        # Debug and Fix editting User.
        # try:
        #     if main_mail:
        #         user = User.query.filter_by(email=main_mail).first()
        #         admin = Admin.query.filter_by(email=main_mail).first()
        #         print(main_mail)
        #         if user:
        #             print(user)
        #             print(user.personal_data)
        #             print(user.email)
        #             form.email.data = user.email
        #             form.surname.data = user.personal_data.surname
        #             form.other_names.data = user.personal_data.other_names
        #             # form.dob.data = user.personal_data.dob
        #             form.id_number.data = user.personal_data.id_number
        #             form.phone_number.data = user.personal_data.telephone_no
        #             form.address.data = user.personal_data.address
        #             form.postal_code.data = user.personal_data.postal_code
        #             form.gender.data = user.personal_data.gender
        #         elif admin:
        #             print(admin)
        #             print(admin.personal_data)
        #             print(user.email)
        #             form.email.data = admin.email
        #             form.surname.data = admin.personal_data.surname
        #             form.other_names.data = admin.personal_data.other_names
        #             # form.dob.data = admin.personal_data.dob
        #             form.id_number.data = admin.personal_data.id_number
        #             form.phone_number.data = admin.personal_data.telephone_no
        #             form.address.data = admin.personal_data.address
        #             form.postal_code.data = admin.personal_data.postal_code
        #             form.gender.data = admin.personal_data.gender
        #     else:
        #         print("No user found!")
        # except AttributeError:
        #     abort(404, description="Please comlete your registration. Contact the Amin team")
    
    else:
        print("Form Failed")
        logging.debug(f"Current User: {current_user.is_authenticated}")        
    return render_template("user/applicationform.html", form=form, title="Application Form") 


# Admin Section
@app.route("/admin")
@login_required
@role_required('admin')
def admin_index():
    member_count = User.query.count()
    staff_count = Admin.query.count()
    notifications = Notification.query.filter_by(is_read=False).all()
    pending_loan_count = Loan.query.filter_by(status='Pending').count()
    approved_loan_count = Loan.query.filter_by(status='Approved').count()
    loan_notifications = LoanNotification.query.filter_by(is_processed=False).all()

    return render_template("admin/index.html", staff_count=staff_count, member_count=member_count,
                           notifications=notifications, loan_notifications=loan_notifications,
                           approved_loan_count=approved_loan_count,pending_loan_count=pending_loan_count,
                           title="Admin Dashboard", logo_name="Admin Panel")


# View User registration state
@app.route("/admin/view_user/<email>")
@login_required
@role_required('admin')
def view_user_data(email):
    user = User.query.filter_by(email=email).first()
    admin = Admin.query.filter_by(email=email).first()
    return render_template("admin/view_user.html", user=user, admin=admin)


# mark Notifications
@app.route("/admin/mark_notification_read/<int:notification_id>", methods=["POST"])
@login_required
@role_required('admin')
def mark_notification_read(notification_id):
    notification = Notification.query.get(notification_id)
    loan_notification = LoanNotification.query.get(notification_id)
    if notification:
        notification.is_read = True
        db.session.commit()

    if loan_notification:
        loan_notification.is_processed = True
        db.session.commit()
    return redirect(url_for("admin_index"))


# Loan Section

@app.route("/admin/loans")
@login_required
@role_required('admin')
def admin_loans():
    loans = Loan.query.count()
    pending_loan_count = Loan.query.filter_by(status='Pending').count()
    approved_loan_count = Loan.query.filter_by(status='Approved').count()
    rejected_loan_count = Loan.query.filter_by(status='Rejected').count()
    return render_template("admin/loans.html", loans=loans, pending_loan_count=pending_loan_count,
                           approved_loan_count=approved_loan_count, rejected_loan_count=rejected_loan_count)


@app.route('/admin/pending_loans')
@role_required('admin')
@login_required
def view_pending_loans():   
    loans = Loan.query.filter_by(status='Pending').all()
    return render_template('admin/pending_loans.html', loans=loans)


@app.route('/admin/approve_loan/<int:loan_id>', methods=['POST'])
@role_required('admin')
@login_required
def approve_loan(loan_id):    
    loan = Loan.query.get_or_404(loan_id)
    user = User.query.get(loan.user_id)

    # Check loan status
    if loan.status != 'Pending':
        flash('Loan has already been processed.', 'danger')
        return redirect(url_for('admin_dashboard'))

    # Perform eligibility checks
    eligibility_errors = []
    
    # Check user's account balance
    user_account = Account.query.filter_by(user_id=user.user_id).first()

    if user_account is None:
        loan.status = 'Rejected'
        loan.rejection_reason = "User account not found."
        flash("User account not found. Please contact support.", 'danger')
        db.session.commit()       
        return redirect(url_for('admin_index'))

        
    if user_account.balance < 1000:  
        eligibility_errors.append('User does not have enough balance to be eligible.')

    # Check if the user has any unpaid loans
    existing_loans = Loan.query.filter_by(user_id=user.user_id, status='Disbursed').all()
    if existing_loans:
        eligibility_errors.append('User has unpaid loans.')

    # Handle eligibility issues
    if eligibility_errors:
        loan.status = 'Rejected'
        loan.rejection_reason = ', '.join(eligibility_errors)
        db.session.commit()
        
        flash('Loan rejected: ' + ', '.join(eligibility_errors), 'danger')
        return redirect(url_for('admin_index'))

    # If all checks pass, approve the loan
    loan.status = 'Approved'
    loan.approved_at = datetime.now()
    db.session.commit()

    flash('Loan approved successfully!', 'success')

    return redirect(url_for('view_pending_loans'))
    

@app.route('/admin/reject_loan/<int:loan_id>', methods=['POST'])
@role_required('admin')
@login_required
def reject_loan(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    loan.status = 'Rejected'
    db.session.add(loan)
    db.session.commit()
    flash('Loan has been rejected.', 'danger')

    return redirect(url_for('view_pending_loans'))
    


# Loan Section
@app.route('/disburse_loan/<int:loan_id>', methods=['POST'])
@role_required('admin')
@login_required
def disburse_loan(loan_id):    
    loan = Loan.query.get_or_404(loan_id)
    
    # Ensure the loan is approved
    if loan.status == 'Approved':
        # Get the user and bank accounts
        user_account = Account.query.filter_by(user_id=loan.user_id).first()
        bank_account = Account.query.filter_by(account_type='Bank').first()

        # Check if the bank has enough funds
        if bank_account.balance >= loan.loan_amount:
            # Deduct from bank and credit user
            bank_account.balance -= loan.loan_amount
            user_account.balance += loan.loan_amount

            # Record the disbursement transaction
            transaction = Transaction(
                loan_id=loan.id,
                transaction_type='Disbursement',
                amount=loan.loan_amount
            )

            # Update loan status to disbursed
            loan.status = 'Disbursed'
            
            # Commit the changes
            db.session.add(transaction)
            db.session.commit()

            flash('Loan disbursed successfully!', 'success')
        else:
            flash('Insufficient funds in the bank account!', 'danger')
    else:
        flash('Loan must be approved before disbursement.', 'danger')
    
    return redirect(url_for('admin_loans'))


@app.route("/admin/members")
@login_required
@role_required('admin')
def admin_members():
    member_count = User.query.count()
    members = User.query.all()

    members_dict = [member.to_dict() for member in members]
    return render_template("admin/members.html", members=members_dict, member_count=member_count,
                           title="Members Management", logo_name="Members Management")


@app.route("/admin/staff")
@login_required
@role_required('admin')
def admin_staff():
    members = Admin.query.all()

    members_dict = [member.to_dict() for member in members]
    return render_template("admin/staff.html", members=members_dict,
                           title="Staff Management", logo_name="Staff Management")


@app.route("/admin/settings")
@login_required
@role_required('admin')
def admin_settings():
    return render_template("admin/settings.html", title="Settings - Admin Dashboard", logo_name="Admin Panel")


@app.route("/admin/reports")
@login_required
@role_required('admin')
def admin_reports():
    member_count = User.query.count()
    approved_loan_count = Loan.query.filter_by(status='Approved').count()
    loans = Loan.query.count()

    return render_template("admin/reports.html", title="Reports - Admin Dashboard", logo_name="Admin Panel",
                           members=member_count, approved_loan_count=approved_loan_count, loans=loans )
    

# User Section
@app.route("/overview")
@login_required
def home():
    return render_template("user/overview.html", title="Overview | SACCO Dashboard")


@app.route('/apply_for_loan', methods=['POST'])
@login_required
def apply_for_loan():
    # Get form data
    loan_amount = float(request.form['loanAmount'])
    loan_purpose = request.form['loanPurpose']
    monthly_debt = float(request.form['monthly_debt'])
    loan_term = int(request.form['loanTerm'])


    # Check loan eligibility
    is_eligible, reason = check_loan_eligibility(current_user, loan_amount, monthly_debt)

    if not is_eligible:
        flash(f'Loan application denied: {reason}')
        return redirect(url_for('application'))

    # If eligible, save the loan request
    new_loan = Loan(user_id=current_user.user_id, loan_amount=loan_amount, purpose=loan_purpose, loan_term=loan_term)
    db.session.add(new_loan)
    db.session.commit()

    notification = LoanNotification(user_email=current_user.email)
    db.session.add(notification)
    db.session.commit()

    flash('Loan application submitted successfully!')
    return redirect(url_for('loan_application_status'))


@app.route('/loan_application_status')
@login_required
def loan_application_status():
    # get the current user's loans
    loans = Loan.query.filter_by(user_id=current_user.user_id).all()
    return render_template('user/loan_status.html', loans=loans)


@app.route("/application", methods=['POST', 'GET'])
@login_required
def application():
    return render_template("user/loan_application.html", title="Notifications | SACCO Dashboard")



@app.route("/notification")
@login_required
def notification():
    return render_template("user/notifications.html", title="Notifications | SACCO Dashboard")



@app.route("/profile")
@login_required
def profile():
    return render_template("user/profile.html")


def get_next_admin_id():
    current_max = db.session.query(func.max(Admin.admin_id)).scalar()
    next_id = int(current_max.split('_')[1]) + 1 if current_max else 1
    return next_id


def get_next_user_id():
    current_max = db.session.query(func.max(User.user_id)).scalar()
    next_id = int(current_max.split('_')[1]) + 1 if current_max else 1
    return next_id


@app.route("/admin/register", methods=['POST', 'GET'])
def admin_register():
    if current_user.is_authenticated:
        return redirect(url_for('admin_index'))
    form = AdminRegistrationForm()
    if form.validate_on_submit():
        email=request.form.get('email')
        hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        admin = Admin(admin_id=f'admin_{get_next_admin_id()}', username=form.username.data, email=form.email.data, password=hash_pw, role=form.role.data)
        db.session.add(admin)
        db.session.commit()

        notification = Notification(user_email=email)
        db.session.add(notification)
        db.session.commit()
        flash("Your Account Has been created succesfully!")
        return redirect(url_for('login'))
    return render_template("user/registration.html", form=form)


@app.route("/register", methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        email=request.form.get('email')
        hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(user_id=f'user_{get_next_user_id()}', username=form.username.data, email=form.email.data, password=hash_pw, role=form.role.data)
        db.session.add(user)
        db.session.commit()

        user_account = Account(user_id=user.user_id, balance=500.0, deposit_method="Mobile Money", reference_no="Ref_001", account_type='User')
        db.session.add(user_account)
        db.session.commit()

        notification = Notification(user_email=email)
        db.session.add(notification)
        db.session.commit()
        flash("Your Account Has been created succesfully!")
        return redirect(url_for('login'))
    return render_template("user/registration.html", form=form)



@app.route("/login", methods=['POST', 'GET'])
def login():   
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        admin = Admin.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user) # TODO: Implement remember me.
            next_page = request.args.get('next')
            flash("Sign In successfully!")
            return redirect(next_page) if next_page else redirect(url_for('home'))
        elif admin and bcrypt.check_password_hash(admin.password, form.password.data):
            login_user(admin) # TODO: Implement remember me.
            # if not user.personal_data:
            #     return redirect(url_for('personal_data'))           
            next_page = request.args.get('next')    # Get next page in the url query
            flash("Sign In successfully!")
            return redirect(next_page) if next_page else redirect(url_for('admin_index'))
        else:
            flash("Log In unsuccessful, please check email and password!")
    return render_template("user/login.html", form=form)


@app.route("/logout")   # TODO Update Log Out Icon
def logout():
    logout_user()
    return redirect('login')

def get_next_ref_id():
    current_max = db.session.query(func.max(Account.reference_no)).scalar()
    next_id = int(current_max.split('_')[1]) + 1 if current_max else 1
    return next_id

@app.route("/deposit", methods=['POST', 'GET'])
@login_required
def deposit():
    if request.method == 'POST':
        if 'amount' in request.form and 'deposit_method' in request.form and 'account' in request.form:
            deposit_amount = float(request.form['amount'])
            deposit_method = request.form['deposit_method']
            account_type = request.form['account']
            reference_no = f'Ref_{get_next_ref_id()}'

            user_account = Account.query.filter_by(user_id=current_user.user_id).first()
            user_account.balance += deposit_amount
                
            # Record the deposit transaction
                
            deposit = Deposit(user_id=current_user.user_id, amount=deposit_amount,
                            deposit_method=deposit_method, account_type=account_type,
                            reference_no=reference_no)
            
            db.session.add(deposit)
            db.session.commit()
    elif request.method == 'GET':
        user_deposits = Deposit.query.filter_by(user_id=current_user.user_id).all()

    return render_template("user/deposits.html", title="Deposits | SACCO Dashboard",
                           deposits=user_deposits)


# @app.route("/transaction", methods=['POST', 'GET'])
# @login_required
# def transaction():
#     return render_template("user/transactions.html", title="Transactions | SACCO Dashboard")

@app.route("/withdraw", methods=['POST'])
@login_required
def withdraw():
    if request.method == 'POST':
        if 'amount' in request.form and 'withdrawal_method' in request.form and 'account' in request.form:
            withdrawal_amount = float(request.form['amount'])
            withdrawal_method = request.form['withdrawal_method']
            account_type = request.form['account']
            reference_no = f'Ref_{get_next_ref_id()}'
            
            # transaction fee
            transaction_fee = 0.02 * withdrawal_amount
            total_deducted = withdrawal_amount + transaction_fee
            
            # Check if the user has sufficient funds
            user_account = Account.query.filter_by(user_id=current_user.user_id).first()
            if user_account.balance >= total_deducted:
                # Deduct total amount (withdrawal + fee) from user's account
                user_account.balance -= total_deducted
                
                # Record the withdrawal transaction
                withdrawal = Withdrawals(user_id=current_user.user_id,
                                        amount=withdrawal_amount,
                                        withdrawal_method=withdrawal_method,
                                        account_type=account_type,
                                        transaction_fee=transaction_fee,
                                        total_deducted=total_deducted,
                                        reference_no=reference_no)
                
                db.session.add(withdrawal)
                db.session.commit()

                return redirect(url_for('show_withdrawals'))
            else:
                flash("Insufficient funds.", "error")
                return redirect(url_for('show_withdrawals'))
    elif request.method == 'GET':
        withdrawals = Withdrawals.query.filter_by(user_id=current_user.user_id).all()
    return render_template("user/withdraws.html", title="Withdraw | SACCO Dashboard",
                           withdrawals=withdrawals)


@app.route("/statements", methods=['POST', 'GET'])
@login_required
def statements():
    return render_template("user/statements.html", title="Statements | SACCO Dashboard")


@app.route("/news", methods=['POST', 'GET'])
@login_required
def news():
    return render_template("user/news.html", title="News/Announcements | SACCO Dashboard")


@app.route("/support", methods=['POST', 'GET'])
@login_required
def support():
    return render_template("user/support.html", title="Support | SACCO Dashboard")


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    # html_msg = render_template('password_reset.html', user=user, token=token)
    # msg.html = html_msg
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)



@app.route("/reset_password", methods=['POST', 'GET'])
def reset_request():
     if current_user.is_authenticated:
        return redirect(url_for('home'))
     form = ResetPasswordRequestForm()
     if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        admin = Admin.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        elif admin:
            send_password_reset_email(admin)
        flash('An email with reset instuction has been sent to your email', 'info') 
        return redirect(url_for('login'))
     return render_template('user/reset_request.html', form=form)

@app.route("/reset_password/<token>", methods=['POST', 'GET'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_password_token(token)
    admin = Admin.verify_reset_password_token(token)
    if user is None:
        flash('Invalid or Expired Token', 'danger')
        return redirect(url_for('reset_request'))
    elif admin is None:
        flash('Invalid or Expired Token', 'danger')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hash_pw
        admin.password = hash_pw
        db.session.commit()
        flash("Your password has been updated! You are now able to sign in")
        return redirect(url_for('login'))
    return render_template('user/reset_password.html', form=form)


@app.route("/update_password", methods=['POST', 'GET'])
@login_required
def update_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.current_password.data):
            hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            current_user.password = hash_pw
            db.session.commit()
            flash("Your password has been updated!")
            return redirect(url_for('profile'))
        else:
            flash('Old password is incorrect', 'danger')
    return render_template("user/changePassword.html", form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.split(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/assets', picture_fn)

    output_size = (125, 125)
    new_image = Image.open(form_picture)
    new_image.thumbnail(output_size)
    new_image.save(picture_path)

    return picture_fn


def save_identification(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.split(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/identification', picture_fn)

    output_size = (125, 125)
    new_image = Image.open(form_picture)
    new_image.thumbnail(output_size)
    new_image.save(picture_path)

    return picture_fn

@app.route("/update_acount", methods=['POST', 'GET'])
@login_required
def update_account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if not current_user.personal_data:
            flash("You need to complete your registration before updating your profile.", 'warning')
            return redirect(url_for('profile'))
        
        if form.user_profile.data:
            picture_file = save_picture(form.user_profile.data)
            current_user.personal_data.user_profile = picture_file
        current_user.username = form.username.data
        db.session.commit()
        flash("Your account has been updated!")
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    try:
        # Attempt to retrieve the user's profile image
        image_file = url_for('static', filename='assets/' + current_user.personal_data.user_profile)
    except AttributeError:
        # Handle the case where the user has no personal data
        flash("You do not have personal data. Please contact the admin.", 'warning')
        image_file = url_for('static', filename='assets/user.jpeg')  # Use a default image
    return render_template("user/updateUser.html", form=form, image_file=image_file)



@app.route("/personal_data", methods=['POST', 'GET'])
# @login_required
def personal_data():
    form = ApplicationForm()
    if form.validate_on_submit():
        p_data = Admin_personalData(user_id=current_user.user_id, surname=form.surname.data, other_names=form.other_names.data, dob=form.dob.data,
                                   id_number=form.id_number.data, telephone_no=form.phone_number.data, address=form.address.data,
                                   postal_code=form.postal_code.data, gender=form.gender.data, income=form.income.data)
        
        # Save passport photo
        if form.passport_photo.data:
            passport_photo_file = save_picture(form.passport_photo.data)
            p_data.user_profile = passport_photo_file
        
        # Save copy of ID card/passport
        if form.copy_photo.data:
            copy_photo_file = save_identification(form.copy_photo.data)
            p_data.id_profile = copy_photo_file

        try:
            db.session.add(p_data)
            db.session.commit()
            flash("Personal data saved successfully!")
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            print("Error saving personal data: " + str(e), "danger")
    return render_template("user/applicationform.html", form=form, title="Application Form")


# Function to calculate DTI ratio
def calculate_dti(monthly_debt, monthly_income):
    return monthly_debt / monthly_income


MAX_DTI = 0.4  # 40% Debt-to-Income Ratio
MIN_INCOME = 25000  # Minimum annual income for loan

# Function to check eligibility
def check_loan_eligibility(user, loan_amount, monthly_debt):
    monthly_income = user.personal_data.income / 12  # Convert annual income to monthly
    dti = calculate_dti(monthly_debt, monthly_income)

    if dti > MAX_DTI:
        return False, 'Debt-to-Income ratio too high'
    if user.personal_data.income < MIN_INCOME:
        return False, 'Income too low'
    if loan_amount > (user.personal_data.income * 0.5):  # Loan should not exceed 50% of annual income
        return False, 'Loan amount too high compared to income'

    return True, 'Eligible'


