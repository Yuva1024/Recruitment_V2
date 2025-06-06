import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
import jinja2
import markupsafe

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

# Initialize extensions
db = SQLAlchemy(model_class=Base)
csrf = CSRFProtect()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    # Create and configure the app
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    
    # Set secret key from environment or use default for development
    app.secret_key = os.environ.get("SESSION_SECRET", "dev_key")
    
    # Configure middleware
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    # Initialize extensions with the app
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Configure login
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    # Add custom jinja2 filters
    @app.template_filter('nl2br')
    def nl2br_filter(s):
        if not s:
            return ""
        return markupsafe.Markup(s.replace('\n', '<br>'))
    
    # Create upload directories if they don't exist
    os.makedirs(os.path.join(app.static_folder, 'uploads'), exist_ok=True)
    os.makedirs(os.path.join(app.static_folder, 'uploads', 'resumes'), exist_ok=True)
    os.makedirs(os.path.join(app.static_folder, 'uploads', 'logos'), exist_ok=True)
    
    # Serve uploaded files with proper content disposition
    @app.route('/uploads/<path:filename>')
    def serve_upload(filename):
        from flask import send_from_directory, abort, current_app, request, Response
        import mimetypes
        
        # Security check - only allow access to files in the uploads directory
        if '..' in filename:
            abort(403)  # Forbidden
        
        # Debug logs
        logging.info(f"Attempting to serve file: {filename}")
        
        # Path construction - handle 'uploads/' prefix if present 
        if filename.startswith('uploads/'):
            filename = filename[8:]  # Remove 'uploads/' prefix
        
        file_path = os.path.join(current_app.static_folder, 'uploads', filename)
        logging.info(f"Full file path: {file_path}")
        logging.info(f"File exists: {os.path.exists(file_path)}")
        
        try:
            if os.path.exists(file_path):
                # Check if it's a PDF file
                is_pdf = file_path.lower().endswith('.pdf')
                
                # Check if this is a download request (via the download parameter)
                is_download = request.args.get('download', '').lower() in ('true', '1', 'yes')
                
                # Set content disposition based on parameters
                if is_download:
                    disposition = 'attachment'
                else:
                    # For PDFs in iframe context, force inline viewing
                    disposition = 'inline'
                
                logging.info(f"Serving {filename} with disposition: {disposition}")
                
                # Let's handle PDFs and other documents with explicit content-disposition
                return send_from_directory(
                    os.path.dirname(file_path),
                    os.path.basename(file_path),
                    as_attachment=(disposition == 'attachment'),
                    download_name=os.path.basename(filename) if disposition == 'attachment' else None
                )
            else:
                current_app.logger.error(f"File not found: {file_path}")
                abort(404)
        except Exception as e:
            current_app.logger.error(f"Error serving file {filename}: {str(e)}")
            abort(404)
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.jobs import jobs_bp
    from routes.profiles import profiles_bp
    from routes.applications import applications_bp
    from routes.admin import admin_bp
    from routes.contact import contact_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(profiles_bp)
    app.register_blueprint(applications_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(contact_bp)
    
    # Import models for database creation
    with app.app_context():
        import models
        db.create_all()
    
    # Load user for login manager
    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.query.get(int(user_id))
    
    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500
    
    return app

# Import at the end to avoid circular imports
from flask import render_template

# Create the application instance
app = create_app()

# Route for the homepage
@app.route('/')
def index():
    from models import Job
    recent_jobs = Job.query.order_by(Job.created_at.desc()).limit(5).all()
    return render_template('index.html', recent_jobs=recent_jobs)
