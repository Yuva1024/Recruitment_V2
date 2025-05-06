from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from models import User, Job, Application, Contact, Role, CandidateProfile, EmployerProfile

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Admin access middleware
@admin_bp.before_request
def require_admin():
    if not current_user.is_authenticated or current_user.role != Role.ADMIN:
        abort(403)

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    # Get counts for dashboard statistics
    user_count = User.query.count()
    job_count = Job.query.count()
    application_count = Application.query.count()
    message_count = Contact.query.count()
    
    # Get recent items
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_jobs = Job.query.order_by(Job.created_at.desc()).limit(5).all()
    recent_applications = Application.query.order_by(Application.created_at.desc()).limit(5).all()
    unread_messages = Contact.query.filter_by(is_read=False).count()
    
    return render_template('admin/dashboard.html', 
                          user_count=user_count,
                          job_count=job_count,
                          application_count=application_count,
                          message_count=message_count,
                          recent_users=recent_users,
                          recent_jobs=recent_jobs,
                          recent_applications=recent_applications,
                          unread_messages=unread_messages,
                          title='Admin Dashboard')

@admin_bp.route('/users')
@login_required
def users():
    # Get sorting parameters
    sort_by = request.args.get('sort_by', 'created_at')
    order = request.args.get('order', 'desc')
    
    # Get filter parameters
    role_filter = request.args.get('role', '')
    
    # Base query
    query = User.query
    
    # Apply filters
    if role_filter:
        query = query.filter_by(role=role_filter)
    
    # Apply sorting
    if order == 'asc':
        query = query.order_by(getattr(User, sort_by).asc())
    else:
        query = query.order_by(getattr(User, sort_by).desc())
    
    # Get paginated results
    page = request.args.get('page', 1, type=int)
    users = query.paginate(page=page, per_page=20, error_out=False)
    
    return render_template('admin/users.html', 
                          users=users,
                          sort_by=sort_by,
                          order=order,
                          role_filter=role_filter,
                          title='Manage Users')

@admin_bp.route('/users/<int:user_id>/toggle-active', methods=['POST'])
@login_required
def toggle_user_active(user_id):
    user = User.query.get_or_404(user_id)
    
    # Don't allow deactivating yourself
    if user.id == current_user.id:
        flash('You cannot deactivate your own account', 'warning')
        return redirect(url_for('admin.users'))
    
    user.is_active = not user.is_active
    status = 'activated' if user.is_active else 'deactivated'
    
    try:
        db.session.commit()
        flash(f'User {user.username} has been {status}', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating user: {str(e)}', 'danger')
    
    return redirect(url_for('admin.users'))

@admin_bp.route('/jobs')
@login_required
def jobs():
    # Get sorting parameters
    sort_by = request.args.get('sort_by', 'created_at')
    order = request.args.get('order', 'desc')
    
    # Get filter parameters
    active_only = request.args.get('active_only', 'false') == 'true'
    
    # Base query
    query = Job.query
    
    # Apply filters
    if active_only:
        query = query.filter_by(is_active=True)
    
    # Apply sorting
    if order == 'asc':
        query = query.order_by(getattr(Job, sort_by).asc())
    else:
        query = query.order_by(getattr(Job, sort_by).desc())
    
    # Get paginated results
    page = request.args.get('page', 1, type=int)
    jobs = query.paginate(page=page, per_page=20, error_out=False)
    
    return render_template('admin/jobs.html', 
                          jobs=jobs,
                          sort_by=sort_by,
                          order=order,
                          active_only=active_only,
                          title='Manage Jobs')

@admin_bp.route('/applications')
@login_required
def applications():
    # Get sorting parameters
    sort_by = request.args.get('sort_by', 'created_at')
    order = request.args.get('order', 'desc')
    
    # Get filter parameters
    status_filter = request.args.get('status', '')
    
    # Base query
    query = Application.query
    
    # Apply filters
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    # Apply sorting
    if order == 'asc':
        query = query.order_by(getattr(Application, sort_by).asc())
    else:
        query = query.order_by(getattr(Application, sort_by).desc())
    
    # Get paginated results
    page = request.args.get('page', 1, type=int)
    applications = query.paginate(page=page, per_page=20, error_out=False)
    
    # Get related jobs for each application
    application_jobs = {}
    for application in applications.items:
        job = Job.query.get(application.job_id)
        application_jobs[application.id] = job
    
    return render_template('admin/applications.html', 
                          applications=applications,
                          application_jobs=application_jobs,
                          sort_by=sort_by,
                          order=order,
                          status_filter=status_filter,
                          title='Manage Applications')

@admin_bp.route('/contact-messages')
@login_required
def contact_messages():
    # Get sorting parameters
    sort_by = request.args.get('sort_by', 'created_at')
    order = request.args.get('order', 'desc')
    
    # Get filter parameters
    unread_only = request.args.get('unread_only', 'false') == 'true'
    
    # Base query
    query = Contact.query
    
    # Apply filters
    if unread_only:
        query = query.filter_by(is_read=False)
    
    # Apply sorting
    if order == 'asc':
        query = query.order_by(getattr(Contact, sort_by).asc())
    else:
        query = query.order_by(getattr(Contact, sort_by).desc())
    
    # Get paginated results
    page = request.args.get('page', 1, type=int)
    messages = query.paginate(page=page, per_page=20, error_out=False)
    
    return render_template('admin/contact_messages.html', 
                          messages=messages,
                          sort_by=sort_by,
                          order=order,
                          unread_only=unread_only,
                          title='Contact Messages')

@admin_bp.route('/contact-messages/<int:message_id>')
@login_required
def view_message(message_id):
    message = Contact.query.get_or_404(message_id)
    
    # Mark as read if it wasn't already
    if not message.is_read:
        message.is_read = True
        db.session.commit()
    
    return render_template('admin/view_message.html', 
                          message=message,
                          title='View Message')
