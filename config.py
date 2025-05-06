import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Database configuration
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
if not SQLALCHEMY_DATABASE_URI:
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.environ.get('PGUSER')}:{os.environ.get('PGPASSWORD')}@{os.environ.get('PGHOST')}:{os.environ.get('PGPORT')}/{os.environ.get('PGDATABASE')}"

# SQLAlchemy connection pool settings
SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
    "pool_timeout": 30,
    "max_overflow": 15,
    "pool_size": 5,
    "connect_args": {"connect_timeout": 10}
}
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask configuration
SECRET_KEY = os.environ.get('SESSION_SECRET', 'dev_key')
DEBUG = True

# Upload configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
