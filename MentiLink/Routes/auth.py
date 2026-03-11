from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from database import db
from models.session import Session

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'] 
        password = request.form['password']

        user = User.query.filter_by(email=email).first()  

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash('Invalid email or password')

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get the fields that the form is actually sending
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form['role']
        bio = request.form.get('bio', '')

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('auth.register'))

        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash('Email address already exists')
            return redirect(url_for('auth.register'))

        # Create full_name and a unique username (e.g., from the email)
        full_name = f"{first_name} {last_name}"
        username = email.split('@')[0] # Creates a username from the email prefix

        # Create new user
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            role=role,
            full_name=full_name,
            bio=bio
        )

        db.session.add(user)
        db.session.commit()

        flash('Registration successful! Please login.')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


from flask_login import current_user

@auth_bp.route('/profile/<int:user_id>')
@login_required
def view_profile(user_id):
    # Prevent users from viewing their own profile via this public link
    if user_id == current_user.id:
        return redirect(url_for('auth.profile'))

    user_to_view = User.query.get_or_404(user_id)
    is_authorized = False

    # --- UPDATED AUTHORIZATION LOGIC ---
    # Rule 1: Anyone can view a mentor's profile.
    if user_to_view.role == 'mentor':
        is_authorized = True
    
    # Rule 2: To view a student's profile, you must be their mentor in a session.
    elif user_to_view.role == 'student' and current_user.role == 'mentor':
        session_exists = Session.query.filter_by(mentor_id=current_user.id, student_id=user_to_view.id).first()
        if session_exists:
            is_authorized = True

    if not is_authorized:
        flash('You are not authorized to view this profile.', 'danger')
        return redirect(url_for('dashboard.dashboard'))

    return render_template('view_profile.html', user=user_to_view)

# In Routes/auth.py (add this to the end of the file)

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # Get form data
        current_user.full_name = request.form.get('full_name')
        current_user.phone = request.form.get('phone')
        current_user.bio = request.form.get('bio')
        current_user.qualification = request.form.get('qualification')
        current_user.field_of_study = request.form.get('field_of_study')
        
        # Update expertise only if the user is a mentor
        if current_user.role == 'mentor':
            current_user.expertise = request.form.get('expertise')
            
        db.session.commit()
        flash('Your profile has been updated successfully!', 'success')
        return redirect(url_for('auth.profile'))
        
    return render_template('profile.html')