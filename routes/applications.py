from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from models import Application, Job, CandidateProfile, EmployerProfile, User, Role
from forms.applications import JobApplicationForm, ApplicationStatusForm
from utils.file_handler import save_file

applications_bp = Blueprint('applications', __name__, url_prefix='/applications')

@applications_bp.route('/job/<int:job_id>/apply', methods=['GET', 'POST'])
@login_required
def apply(job_id):
    # Only candidates can apply for jobs
    if current_user.role != Role.CANDIDATE:
        flash('Only candidates can apply for jobs', 'warning')
        return redirect(url_for('jobs.show', job_id=job_id))
    
    job = Job.query.get_or_404(job_id)
    
    # Check if user has already applied
    existing_application = Application.query.filter_by(
        job_id=job.id, 
        candidate_id=current_user.id
    ).first()
    
    if existing_application:
        flash('You have already applied for this job', 'info')
        return redirect(url_for('jobs.show', job_id=job.id))
    
    form = JobApplicationForm()
    
    if form.validate_on_submit():
        # Get candidate profile to use existing resume if available and none provided
        profile = CandidateProfile.query.filter_by(user_id=current_user.id).first()
        
        resume_path = None
        
        # If resume uploaded with application, use it
        if form.resume.data:
            resume_path = save_file(form.resume.data, 'uploads/resumes')
        # Otherwise use resume from profile if it exists
        elif profile and profile.resume_path:
            resume_path = profile.resume_path
        
        if not resume_path:
            flash('Please upload a resume with your application', 'warning')
            return render_template('applications/create.html', form=form, job=job)
        
        application = Application(
            job_id=job.id,
            candidate_id=current_user.id,
            resume_path=resume_path,
            cover_letter=form.cover_letter.data,
            status='pending'
        )
        
        db.session.add(application)
        
        try:
            db.session.commit()
            flash('Your application has been submitted successfully!', 'success')
            return redirect(url_for('profiles.candidate_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error submitting application: {str(e)}', 'danger')
    
    return render_template('applications/create.html', 
                          form=form, 
                          job=job,
                          title='Apply for Job')

@applications_bp.route('/my-applications')
@login_required
def my_applications():
    # Only candidates can view their applications
    if current_user.role != Role.CANDIDATE:
        flash('Access denied', 'warning')
        return redirect(url_for('index'))
    
    applications = Application.query.filter_by(candidate_id=current_user.id) \
                              .order_by(Application.created_at.desc()) \
                              .all()
    
    return render_template('applications/index.html', 
                          applications=applications,
                          title='My Applications')

@applications_bp.route('/job/<int:job_id>/applications')
@login_required
def job_applications(job_id):
    job = Job.query.get_or_404(job_id)
    
    # Only the employer who posted the job or an admin can view applications
    if job.employer_id != current_user.id and current_user.role != Role.ADMIN:
        abort(403)
    
    applications = Application.query.filter_by(job_id=job.id) \
                              .order_by(Application.created_at.desc()) \
                              .all()
    
    # Get candidate profiles for the applications
    application_profiles = {}
    for application in applications:
        profile = CandidateProfile.query.filter_by(user_id=application.candidate_id).first()
        application_profiles[application.id] = profile
    
    return render_template('applications/job_applications.html', 
                          applications=applications,
                          job=job,
                          profiles=application_profiles,
                          title=f'Applications for {job.title}')

@applications_bp.route('/<int:application_id>')
@login_required
def show(application_id):
    application = Application.query.get_or_404(application_id)
    job = Job.query.get(application.job_id)
    
    # Only the applicant, the employer who posted the job, or an admin can view the application
    if not (current_user.id == application.candidate_id or 
            current_user.id == job.employer_id or 
            current_user.role == Role.ADMIN):
        abort(403)
    
    # Get candidate profile
    candidate = User.query.get(application.candidate_id)
    profile = CandidateProfile.query.filter_by(user_id=candidate.id).first()
    
    return render_template('applications/show.html', 
                          application=application,
                          job=job,
                          candidate=candidate,
                          profile=profile,
                          title='Application Details')

@applications_bp.route('/<int:application_id>/update-status', methods=['POST'])
@login_required
def update_status(application_id):
    application = Application.query.get_or_404(application_id)
    job = Job.query.get(application.job_id)
    
    # Only the employer who posted the job or an admin can update the status
    if not (current_user.id == job.employer_id or current_user.role == Role.ADMIN):
        abort(403)
    
    # Get status from form
    status = request.form.get('status')
    
    if status not in ['pending', 'reviewed', 'interviewed', 'offered', 'rejected']:
        flash('Invalid status', 'danger')
        return redirect(url_for('applications.show', application_id=application.id))
    
    application.status = status
    
    try:
        db.session.commit()
        flash('Application status updated successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating status: {str(e)}', 'danger')
    
    return redirect(url_for('applications.show', application_id=application.id))
