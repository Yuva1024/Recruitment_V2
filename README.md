# CareerConnect - Recruitment Platform

A comprehensive Python Flask-based recruitment platform that streamlines job searching, application management, and hiring processes.

## Features

- User authentication with role-based access (Candidates, Employers, Admins)
- Job posting and management for employers
- Advanced job search and filtering
- Application tracking system
- Profile management for both candidates and employers
- Resume/CV uploads
- Admin dashboard for site management

## Tech Stack

- **Backend**: Python Flask
- **Database**: PostgreSQL (with SQLite fallback for local development)
- **ORM**: SQLAlchemy
- **Frontend**: Bootstrap CSS, Vanilla JavaScript
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **File Management**: Werkzeug

## Local Development Setup

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Git (optional, for cloning)

### Step 1: Get the Project
Either download the project as a ZIP file or clone the repository:
```bash
git clone <repository-url>
cd careerconnect
```

### Step 2: Set Up a Virtual Environment
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
# Create requirements.txt file
cat > requirements.txt << EOF
flask
flask-login
flask-migrate
flask-sqlalchemy
flask-wtf
email-validator
gunicorn
werkzeug
markupsafe
jinja2
EOF

# Install requirements
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
# Set Flask environment variables (optional)
export FLASK_APP=main.py
export FLASK_ENV=development

# Run the application
python -m flask run
# OR
gunicorn --bind 127.0.0.1:5000 main:app
```

The application will be accessible at [http://127.0.0.1:5000](http://127.0.0.1:5000)

### Database Configuration
By default, the application will use SQLite for local development. The database file (`careerconnect.db`) will be created automatically in the project root directory.

If you want to use PostgreSQL:
```bash
# Set PostgreSQL environment variables
export DATABASE_URL=postgresql://username:password@localhost:5432/dbname
```

### Create an Admin User
After registering a user, you can promote them to admin by directly editing the SQLite database:
```bash
sqlite3 careerconnect.db
# In SQLite prompt:
UPDATE user SET role = 'admin' WHERE id = 1;
.exit
```

## Folder Structure

- `/forms` - Form definitions using Flask-WTF
- `/models` - SQLAlchemy database models
- `/routes` - Flask route handlers
- `/static` - Static assets (CSS, JS, uploads)
- `/templates` - Jinja2 HTML templates
- `/utils` - Utility functions and helpers

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.