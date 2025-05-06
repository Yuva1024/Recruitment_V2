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
    
    # Add a route to serve files from uploads directory (as a backup if static doesn't work)
    @app.route('/files/<path:filename>')
    def uploaded_file(filename):
        from flask import send_from_directory
        return send_from_directory(os.path.join(app.static_folder, 'uploads'), filename)
    
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
