from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from sqlalchemy import or_
from app import db
from models import Job, User, Role, Application
from forms.jobs import JobPostForm, JobSearchForm

jobs_bp = Blueprint('jobs', __name__, url_prefix='/jobs')

@jobs_bp.route('/', methods=['GET'])
def index():
    form = JobSearchForm()
    page = request.args.get('page', 1, type=int)
    
    # Base query
    jobs_query = Job.query.filter_by(is_active=True)
    
    # Apply search filters from form or URL parameters
    keyword = request.args.get('keyword', '')
    location = request.args.get('location', '')
    job_type = request.args.get('job_type', '')
    experience_level = request.args.get('experience_level', '')
    remote = request.args.get('remote', False, type=bool)
    
    # Populate form with search parameters
    form.keyword.data = keyword
    form.location.data = location
    form.job_type.data = job_type
    form.experience_level.data = experience_level
    form.remote.data = remote
    
    # Apply filters
    if keyword:
        jobs_query = jobs_query.filter(
            or_(
                Job.title.ilike(f'%{keyword}%'),
                Job.description.ilike(f'%{keyword}%'),
                Job.company.ilike(f'%{keyword}%')
            )
        )
    
    if location:
        jobs_query = jobs_query.filter(Job.location.ilike(f'%{location}%'))
    
    if job_type:
        jobs_query = jobs_query.filter(Job.job_type == job_type)
    
    if experience_level:
        jobs_query = jobs_query.filter(Job.experience_level == experience_level)
    
    if remote:
        jobs_query = jobs_query.filter(Job.is_remote == True)
    
    # Order by newest first
    jobs_query = jobs_query.order_by(Job.created_at.desc())
    
    # Paginate results
    jobs = jobs_query.paginate(page=page, per_page=10, error_out=False)
    
    return render_template('jobs/index.html', 
                          jobs=jobs, 
                          form=form, 
                          title='Job Listings')

@jobs_bp.route('/<int:job_id>', methods=['GET'])
def show(job_id):
    job = Job.query.get_or_404(job_id)
    
    # Check if user has already applied
    has_applied = False
    if current_user.is_authenticated and current_user.role == Role.CANDIDATE:
        application = Application.query.filter_by(
            job_id=job.id, 
            candidate_id=current_user.id
        ).first()
        has_applied = application is not None
    
    return render_template('jobs/show.html', 
                          job=job, 
                          has_applied=has_applied,
                          title=job.title)

@jobs_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    # Only employers can create job listings
    if current_user.role != Role.EMPLOYER:
        flash('Only employers can post jobs', 'warning')
        return redirect(url_for('jobs.index'))
    
    form = JobPostForm()
    
    if form.validate_on_submit():
        job = Job(
            title=form.title.data,
            company=form.company.data,
            location=form.location.data,
            description=form.description.data,
            requirements=form.requirements.data,
            salary_range=form.salary_range.data,
            job_type=form.job_type.data,
            experience_level=form.experience_level.data,
            education_level=form.education_level.data,
            industry=form.industry.data,
            is_remote=form.is_remote.data,
            closing_date=form.closing_date.data,
            employer_id=current_user.id
        )
        
        db.session.add(job)
        
        try:
            db.session.commit()
            flash('Job posted successfully!', 'success')
            return redirect(url_for('jobs.show', job_id=job.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error posting job: {str(e)}', 'danger')
    
    return render_template('jobs/create.html', form=form, title='Post a Job')

@jobs_bp.route('/<int:job_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(job_id):
    job = Job.query.get_or_404(job_id)
    
    # Only the employer who created the job or an admin can edit it
    if job.employer_id != current_user.id and current_user.role != Role.ADMIN:
        abort(403)
    
    form = JobPostForm()
    
    if form.validate_on_submit():
        job.title = form.title.data
        job.company = form.company.data
        job.location = form.location.data
        job.description = form.description.data
        job.requirements = form.requirements.data
        job.salary_range = form.salary_range.data
        job.job_type = form.job_type.data
        job.experience_level = form.experience_level.data
        job.education_level = form.education_level.data
        job.industry = form.industry.data
        job.is_remote = form.is_remote.data
        job.closing_date = form.closing_date.data
        
        try:
            db.session.commit()
            flash('Job updated successfully!', 'success')
            return redirect(url_for('jobs.show', job_id=job.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating job: {str(e)}', 'danger')
    
    elif request.method == 'GET':
        # Populate form with current job data
        form.title.data = job.title
        form.company.data = job.company
        form.location.data = job.location
        form.description.data = job.description
        form.requirements.data = job.requirements
        form.salary_range.data = job.salary_range
        form.job_type.data = job.job_type
        form.experience_level.data = job.experience_level
        form.education_level.data = job.education_level
        form.industry.data = job.industry
        form.is_remote.data = job.is_remote
        form.closing_date.data = job.closing_date
    
    return render_template('jobs/edit.html', form=form, job=job, title='Edit Job')

@jobs_bp.route('/<int:job_id>/delete', methods=['POST'])
@login_required
def delete(job_id):
    job = Job.query.get_or_404(job_id)
    
    # Only the employer who created the job or an admin can delete it
    if job.employer_id != current_user.id and current_user.role != Role.ADMIN:
        abort(403)
    
    try:
        db.session.delete(job)
        db.session.commit()
        flash('Job listing deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting job: {str(e)}', 'danger')
    
    if current_user.role == Role.ADMIN:
        return redirect(url_for('admin.jobs'))
    else:
        return redirect(url_for('profiles.employer_dashboard'))

@jobs_bp.route('/<int:job_id>/toggle-status', methods=['POST'])
@login_required
def toggle_status(job_id):
    job = Job.query.get_or_404(job_id)
    
    # Only the employer who created the job or an admin can change its status
    if job.employer_id != current_user.id and current_user.role != Role.ADMIN:
        abort(403)
    
    job.is_active = not job.is_active
    status = 'active' if job.is_active else 'inactive'
    
    try:
        db.session.commit()
        flash(f'Job listing is now {status}', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating job status: {str(e)}', 'danger')
    
    return redirect(url_for('jobs.show', job_id=job.id))
