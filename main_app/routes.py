from main_app import app, db, bcrypt, mail
from flask import render_template, flash, request, url_for, redirect
from main_app.models import User, User_personalData
from main_app.forms import (RegistrationForm, LoginForm, ApplicationForm,
                            ResetPasswordRequestForm, ResetPasswordForm,
                            ChangePasswordForm, UpdateAccountForm)
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message

@app.route("/overview")
@login_required
def home():
    return render_template("overview.html", title="Overview | SACCO Dashboard")

@app.route("/register", methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hash_pw)
        db.create_all()
        db.session.add(user)
        db.session.commit()
        flash("Your Account Has been created succesfully!")
        return redirect(url_for('login'))
    return render_template("registration.html", form=form)


@app.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # if not user.personal_data_submitted:
            #     return redirect(url_for('personal_data'))
            login_user(user) # TODO: Implement remember me.
            next_page = request.args.get('next')    # Get next page in the url query
            flash("Sign In successfully!")
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Log In unsuccessful, please check email and password!")
    return render_template("login.html", form=form)


@app.route("/logout")   # TODO Update Log Out Icon
def logout():
    logout_user()
    return redirect('login')


@app.route("/personal_data", methods=['POST', 'GET'])
@login_required
def personal_data():
    form = ApplicationForm()
    if form.validate_on_submit():
        user = current_user
        p_data = User_personalData(user_id=current_user.user_id, surname=form.surname.data, other_names=form.other_names.data, dob=form.dob.data,
                                   id_number=form.id_number.data, telephone_no=form.phone_number.data, address=form.address.data,
                                   postal_code=form.postal_code.data, gender=form.gender.data, user=user)
        db.create_all()
        db.session.add(p_data)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("applicationform.html", form=form, title="Application Form")



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
            return redirect(url_for('home'))
        else:
            flash('Old password is incorrect', 'danger')
    return render_template("changePassword.html", form=form)


@app.route("/update_acoount", methods=['POST', 'GET'])
@login_required
def update_account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        db.session.commit()
        flash("Your account has been updated!")
        return redirect(url_for('update_account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template("updateUser.html", form=form)