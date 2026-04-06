from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models import User

auth_bp = Blueprint('auth', __name__)


# login page
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # if already logged in, go to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('tickets.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        # check the fields are filled in
        if not username or not password:
            flash('Please fill in all fields.', 'danger')
            return render_template('login.html')

        # look up the user and check password
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('tickets.dashboard'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')


# registration page
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('tickets.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        # validate all fields are present
        if not username or not email or not password or not confirm:
            flash('Please fill in all fields.', 'danger')
            return render_template('register.html')

        # check password length
        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return render_template('register.html')

        # check passwords match
        if password != confirm:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')

        # check username is not already taken
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return render_template('register.html')

        # check email is not already taken
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return render_template('register.html')

        # create the new user (default role is employee)
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')


# logout
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
