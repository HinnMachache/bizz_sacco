import secrets
import os
import logging
from functools import wraps
from PIL import Image
from main_app import app, db, bcrypt, mail
from flask import render_template, flash, request, url_for, redirect, current_app, abort
from main_app.models import User, User_personalData, Admin, Admin_personalData
from main_app.forms import (RegistrationForm, LoginForm, ApplicationForm,
                            ResetPasswordRequestForm, ResetPasswordForm,
                            ChangePasswordForm, UpdateAccountForm)
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message


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

from main_app import db
from main_app.models import User, Admin


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

# @app.route("/change_user", methods=['POST', 'GET'])
# @login_required
# @role_required('admin')
# def promote_user():
#     form = RegistrationForm()
#     user_admin = User.query.filter_by(email=form.email.data).first()

#     if form.valida
#     if user_admin:
#         promote_user_to_admin(user_admin.user_id)

# Admin Section
@app.route("/admin")
@login_required
# @role_required('admin')
def admin_index():
    member_count = User.query.count()
    staff_count = Admin.query.count()
    return render_template("admin/index.html", staff_count=staff_count, member_count=member_count,
                           title="Admin Dashboard", logo_name="Admin Panel")

@app.route("/admin/loans")
@login_required
# @role_required('admin')
def admin_loans():
    return render_template("admin/loans.html")

@app.route("/admin/members")
@login_required
# @role_required('admin')
def admin_members():
    member_count = User.query.count()
    members = User.query.all()

    members_dict = [member.to_dict() for member in members]
    return render_template("admin/members.html", members=members_dict, member_count=member_count,
                           title="Members Management", logo_name="Members Management")

@app.route("/admin/settings")
@login_required
# @role_required('admin')
def admin_settings():
    return render_template("admin/settings.html", title="Settings - Admin Dashboard", logo_name="Admin Panel")

@app.route("/admin/staff")
@login_required
# @role_required('admin')
def admin_staff():
    return render_template("admin/staff.html", title="Staff Management", logo_name="Staff Management")

@app.route("/admin/reports")
@login_required
# @role_required('admin')
def admin_reports():
    return render_template("admin/reports.html", title="Reports - Admin Dashboard", logo_name="Admin Panel")


# User Section
@app.route("/overview")
@login_required
def home():
    return render_template("user/overview.html", title="Overview | SACCO Dashboard")


@app.route("/application", methods=['POST', 'GET'])
@login_required
def application():
    return render_template("user/notifications.html", title="Notifications | SACCO Dashboard")


@app.route("/notification")
@login_required
def notification():
    return render_template("user/notifications.html", title="Notifications | SACCO Dashboard")


@app.route("/profile")
@login_required
def profile():
    return render_template("user/profile.html")


@app.route("/register", methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        role = form.role.data

        if role == 'user':
            user = User(username=form.username.data, email=form.email.data, password=hash_pw)
            db.session.add(user)
        elif role == 'admin':
            admin = Admin(username=form.username.data, email=form.email.data, password=hash_pw)
            db.session.add(admin)

        db.session.commit()
        flash("Your Account Has been created succesfully!")
        return redirect(url_for('login'))
    return render_template("user/registration.html", form=form)

# Set up logging configuration
logging.basicConfig(filename='app.log', level=logging.DEBUG,  # Set the logging level to DEBUG
                format='%(asctime)s - %(levelname)s - %(message)s') 

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
            logging.debug(f"Current User: {current_user.is_authenticated}")
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

@app.route("/deposit", methods=['POST', 'GET'])
@login_required
def deposit():
    return render_template("user/deposits.html", title="Deposits | SACCO Dashboard")

@app.route("/transaction", methods=['POST', 'GET'])
@login_required
def transaction():
    return render_template("user/transactions.html", title="Transactions | SACCO Dashboard")

@app.route("/withdrawals", methods=['POST', 'GET'])
@login_required
def withdrawals():
    return render_template("user/withdrawals.html", title="Withdrawals | SACCO Dashboard")

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
        if form.user_profile.data:
            picture_file = save_picture(form.user_profile.data)
            current_user.personal_data.user_profile = picture_file
        current_user.username = form.username.data
        db.session.commit()
        flash("Your account has been updated!")
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    image_file = url_for('static', filename='assets/' + current_user.personal_data.user_profile)
    return render_template("user/updateUser.html", form=form, image_file=image_file)



@app.route("/personal_data", methods=['POST', 'GET'])
# @login_required
def personal_data():
    form = ApplicationForm()
    if form.validate_on_submit():
        p_data = User_personalData(user_id=current_user.user_id, surname=form.surname.data, other_names=form.other_names.data, dob=form.dob.data,
                                   id_number=form.id_number.data, telephone_no=form.phone_number.data, address=form.address.data,
                                   postal_code=form.postal_code.data, gender=form.gender.data)
        
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