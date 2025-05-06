from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse
from app import db
from models import User, Role, CandidateProfile, EmployerProfile
from forms.auth import LoginForm, RegistrationForm, PasswordResetRequestForm, PasswordResetForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        
        # Create corresponding profile based on role
        if user.role == Role.CANDIDATE:
            profile = CandidateProfile(
                user=user,
                first_name=form.first_name.data,
                last_name=form.last_name.data
            )
            db.session.add(profile)
        elif user.role == Role.EMPLOYER:
            # Create employer profile with required fields
            profile = EmployerProfile(
                user=user,
                company_name=f"{form.first_name.data} {form.last_name.data}'s Company",  # Temporary name
                company_description="Please update your company description",  # Default placeholder
                location="Please update your location",  # Default placeholder
                contact_email=form.email.data  # Use the registration email
            )
            db.session.add(profile)
        
        db.session.add(user)
        
        try:
            db.session.commit()
            flash('Your account has been created! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating account: {str(e)}', 'danger')
    
    return render_template('auth/register.html', form=form, title='Register')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember.data)
        
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            if user.is_employer():
                next_page = url_for('profiles.employer_dashboard')
            elif user.is_candidate():
                next_page = url_for('profiles.candidate_dashboard')
            else:
                next_page = url_for('admin.dashboard')
        
        return redirect(next_page)
    
    return render_template('auth/login.html', form=form, title='Login')

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # In a real app, would send an email with reset token here
            flash('Check your email for instructions to reset your password', 'info')
            return redirect(url_for('auth.login'))
        else:
            flash('Email not found in our records', 'warning')
    
    return render_template('auth/reset_password_request.html', form=form, title='Reset Password')

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    # In a real app, would verify token here
    user = None
    
    if not user:
        flash('Invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_password_request'))
    
    form = PasswordResetForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', form=form, title='Reset Password')
