import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Database configuration
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

# If no DATABASE_URL is provided, try the PostgreSQL environment variables
if not SQLALCHEMY_DATABASE_URI:
    if all([os.environ.get(var) for var in ['PGUSER', 'PGPASSWORD', 'PGHOST', 'PGPORT', 'PGDATABASE']]):
        # All PostgreSQL variables are present, use them
        SQLALCHEMY_DATABASE_URI = f"postgresql://{os.environ.get('PGUSER')}:{os.environ.get('PGPASSWORD')}@{os.environ.get('PGHOST')}:{os.environ.get('PGPORT')}/{os.environ.get('PGDATABASE')}"
    else:
        # Use SQLite as a fallback
        basedir = os.path.abspath(os.path.dirname(__file__))
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'careerconnect.db')}"
        logging.info(f"Using SQLite database at {os.path.join(basedir, 'careerconnect.db')}")

# SQLAlchemy connection pool settings - only apply to PostgreSQL
if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith('postgresql'):
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
        "pool_timeout": 30,
        "max_overflow": 15,
        "pool_size": 5,
        "connect_args": {"connect_timeout": 10}
    }
else:
    # Simplified options for SQLite
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True
    }
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask configuration
SECRET_KEY = os.environ.get('SESSION_SECRET', 'dev_key')
DEBUG = True

# Upload configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
