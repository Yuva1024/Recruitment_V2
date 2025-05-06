from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from models import CandidateProfile, EmployerProfile, Job, Application, Role
from forms.profiles import CandidateProfileForm, EmployerProfileForm
from utils.file_handler import save_file, delete_file

profiles_bp = Blueprint('profiles', __name__, url_prefix='/profiles')

@profiles_bp.route('/candidate/dashboard')
@login_required
def candidate_dashboard():
    if current_user.role != Role.CANDIDATE:
        flash('Access denied: Not a candidate account', 'warning')
        return redirect(url_for('index'))
    
    # Get profile info
    profile = CandidateProfile.query.filter_by(user_id=current_user.id).first()
    
    # Get applications
    applications = Application.query.filter_by(candidate_id=current_user.id).order_by(Application.created_at.desc()).all()
    
    # Get recent job listings
    recent_jobs = Job.query.filter_by(is_active=True).order_by(Job.created_at.desc()).limit(5).all()
    
    return render_template('profiles/candidate.html', 
                          profile=profile, 
                          applications=applications,
                          recent_jobs=recent_jobs,
                          title='Candidate Dashboard')

@profiles_bp.route('/employer/dashboard')
@login_required
def employer_dashboard():
    if current_user.role != Role.EMPLOYER:
        flash('Access denied: Not an employer account', 'warning')
        return redirect(url_for('index'))
    
    # Get profile info
    profile = EmployerProfile.query.filter_by(user_id=current_user.id).first()
    
    # Get posted jobs
    jobs = Job.query.filter_by(employer_id=current_user.id).order_by(Job.created_at.desc()).all()
    
    # Count applications per job
    job_applications = {}
    for job in jobs:
        job_applications[job.id] = Application.query.filter_by(job_id=job.id).count()
    
    return render_template('profiles/employer.html', 
                          profile=profile, 
                          jobs=jobs,
                          job_applications=job_applications,
                          title='Employer Dashboard')

@profiles_bp.route('/candidate/edit', methods=['GET', 'POST'])
@login_required
def edit_candidate_profile():
    if current_user.role != Role.CANDIDATE:
        flash('Access denied: Not a candidate account', 'warning')
        return redirect(url_for('index'))
    
    profile = CandidateProfile.query.filter_by(user_id=current_user.id).first()
    
    # Create profile if it doesn't exist
    if not profile:
        profile = CandidateProfile(user_id=current_user.id)
        db.session.add(profile)
        db.session.commit()
    
    form = CandidateProfileForm()
    
    if form.validate_on_submit():
        profile.first_name = form.first_name.data
        profile.last_name = form.last_name.data
        profile.phone = form.phone.data
        profile.address = form.address.data
        profile.professional_title = form.professional_title.data
        profile.summary = form.summary.data
        profile.skills = form.skills.data
        profile.experience = form.experience.data
        profile.education = form.education.data
        
        # Resume upload
        if form.resume.data:
            # Delete old resume if exists
            if profile.resume_path:
                delete_file(profile.resume_path)
            
            # Save new resume
            resume_path = save_file(form.resume.data, 'uploads/resumes')
            if resume_path:
                profile.resume_path = resume_path
        
        try:
            db.session.commit()
            flash('Your profile has been updated successfully!', 'success')
            return redirect(url_for('profiles.candidate_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating profile: {str(e)}', 'danger')
    
    elif request.method == 'GET':
        # Populate form with current profile data
        form.first_name.data = profile.first_name
        form.last_name.data = profile.last_name
        form.phone.data = profile.phone
        form.address.data = profile.address
        form.professional_title.data = profile.professional_title
        form.summary.data = profile.summary
        form.skills.data = profile.skills
        form.experience.data = profile.experience
        form.education.data = profile.education
    
    return render_template('profiles/edit.html', 
                          form=form, 
                          profile_type='candidate',
                          title='Edit Candidate Profile')

@profiles_bp.route('/employer/edit', methods=['GET', 'POST'])
@login_required
def edit_employer_profile():
    if current_user.role != Role.EMPLOYER:
        flash('Access denied: Not an employer account', 'warning')
        return redirect(url_for('index'))
    
    profile = EmployerProfile.query.filter_by(user_id=current_user.id).first()
    
    # Create profile if it doesn't exist
    if not profile:
        profile = EmployerProfile(user_id=current_user.id)
        db.session.add(profile)
        db.session.commit()
    
    form = EmployerProfileForm()
    
    if form.validate_on_submit():
        profile.company_name = form.company_name.data
        profile.company_website = form.company_website.data
        profile.company_description = form.company_description.data
        profile.industry = form.industry.data
        profile.company_size = form.company_size.data
        profile.founded_year = form.founded_year.data
        profile.location = form.location.data
        profile.contact_email = form.contact_email.data
        profile.contact_phone = form.contact_phone.data
        
        # Logo upload
        if form.logo.data:
            # Delete old logo if exists
            if profile.logo_path:
                delete_file(profile.logo_path)
            
            # Save new logo
            logo_path = save_file(form.logo.data, 'uploads/logos')
            if logo_path:
                profile.logo_path = logo_path
        
        try:
            db.session.commit()
            flash('Your company profile has been updated successfully!', 'success')
            return redirect(url_for('profiles.employer_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating profile: {str(e)}', 'danger')
    
    elif request.method == 'GET':
        # Populate form with current profile data
        form.company_name.data = profile.company_name
        form.company_website.data = profile.company_website
        form.company_description.data = profile.company_description
        form.industry.data = profile.industry
        form.company_size.data = profile.company_size
        form.founded_year.data = profile.founded_year
        form.location.data = profile.location
        form.contact_email.data = profile.contact_email
        form.contact_phone.data = profile.contact_phone
    
    return render_template('profiles/edit.html', 
                          form=form, 
                          profile_type='employer',
                          title='Edit Employer Profile')

@profiles_bp.route('/view/<int:user_id>')
def view_profile(user_id):
    # Public view of profiles
    from models import User
    
    user = User.query.get_or_404(user_id)
    
    if user.role == Role.CANDIDATE:
        profile = CandidateProfile.query.filter_by(user_id=user.id).first_or_404()
        return render_template('profiles/view_candidate.html', 
                               profile=profile, 
                               user=user,
                               title=f"{profile.first_name} {profile.last_name}'s Profile")
    
    elif user.role == Role.EMPLOYER:
        profile = EmployerProfile.query.filter_by(user_id=user.id).first_or_404()
        # Also get employer's jobs
        jobs = Job.query.filter_by(employer_id=user.id, is_active=True).order_by(Job.created_at.desc()).all()
        return render_template('profiles/view_employer.html', 
                               profile=profile, 
                               user=user, 
                               jobs=jobs,
                               title=f"{profile.company_name}'s Profile")
    
    else:
        flash('Profile not found', 'warning')
        return redirect(url_for('index'))
