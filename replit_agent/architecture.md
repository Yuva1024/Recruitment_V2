# Architecture

## Overview

This repository contains a web-based job board application called CareerConnect that connects employers and job seekers. The application is built using Flask, a Python web framework, with a PostgreSQL database for data persistence. The system follows a monolithic architecture with a clear separation of concerns through blueprints and modular components.

The application serves several user roles (candidates, employers, and administrators) and provides functionality for job posting, application management, user profiles, and administrative tasks.

## System Architecture

### Backend Architecture

The application is built using Flask, a lightweight WSGI web application framework in Python. It follows a modular structure organized around Flask Blueprints to separate different functional areas of the application:

- `auth`: Handles authentication and user management
- `jobs`: Manages job listings and search
- `applications`: Controls job application submission and management
- `profiles`: Manages user profiles for candidates and employers
- `admin`: Provides administrative functionality
- `contact`: Handles contact form submissions

The application utilizes several Flask extensions to enhance functionality:
- `Flask-SQLAlchemy`: ORM for database interactions
- `Flask-Login`: User session management
- `Flask-WTF`: Form handling and CSRF protection
- `Flask-Migrate`: Database migration management

### Frontend Architecture

The frontend uses server-side templating with Jinja2 (Flask's default template engine) to render HTML. The UI is styled using Bootstrap CSS framework (specifically a dark theme version) and Font Awesome for icons.

The application follows a traditional multi-page application (MPA) approach, where different routes render different templates. There's minimal client-side JavaScript, mainly for enhancing user experience with tooltips, popovers, and form validation.

### Data Model

The application uses SQLAlchemy ORM with a well-defined data model:

- `User`: Core user entity with authentication details and role information
- `CandidateProfile`: Extended profile for job seekers
- `EmployerProfile`: Extended profile for employers
- `Job`: Job listing information
- `Application`: Job applications connecting candidates to jobs
- `Contact`: Contact form submissions

The data model implements relationships appropriately (one-to-many, many-to-one) to maintain data integrity while enabling efficient queries.

## Key Components

### Authentication System

The authentication system is built using Flask-Login and implements:
- User registration with role selection (candidate or employer)
- Login with session management
- Password reset functionality
- Role-based access control

The system stores password hashes (not plaintext) using Werkzeug's security functions.

### Job Management

The job management module allows:
- Employers to create, edit, and manage job listings
- Candidates to search and view jobs with filtering capabilities
- Status tracking for job listings (active/inactive)

### Application Management

The application system enables:
- Candidates to apply to jobs with cover letters and resumes
- Employers to review applications
- Status tracking for applications (pending, reviewed, interviewed, offered, rejected)

### Profile Management

The profile system manages:
- Candidate profiles with personal information, skills, experience, and education
- Employer profiles with company information and contact details
- File uploads for resumes and company logos

### Admin Dashboard

The admin section provides:
- Overview of system statistics
- User management
- Job listing moderation
- Application oversight
- Contact message management

### File Handling

The application implements secure file handling for:
- Resume uploads (PDF, DOC, DOCX, TXT)
- Company logo uploads (common image formats)

Files are stored in the filesystem with unique filenames to prevent collisions.

## Data Flow

1. **Authentication Flow**:
   - User registers with email, username, password, and role selection
   - User logs in with credentials
   - System creates and manages user sessions
   - Authorization checks are performed based on user role

2. **Job Posting Flow**:
   - Employer creates job listing with details
   - System stores the job in the database
   - Job appears in listings for candidates
   - Employer can edit or deactivate listings

3. **Job Application Flow**:
   - Candidate views job details
   - Candidate submits application with cover letter and resume
   - Employer reviews applications
   - Employer can update application status

4. **Profile Management Flow**:
   - Users create and edit their profiles
   - Candidates upload resumes
   - Employers upload company logos
   - Profiles are shown to relevant parties (employers see candidate profiles)

## External Dependencies

### Frontend Dependencies
- Bootstrap CSS framework (loaded via CDN)
- Font Awesome icon library (loaded via CDN)

### Backend Dependencies
- Flask and Flask extensions (SQLAlchemy, Login, WTF, Migrate)
- SQLAlchemy for ORM
- Gunicorn for WSGI HTTP server
- Psycopg2 for PostgreSQL integration
- Werkzeug for utilities and middleware
- Email validator for form validation

## Deployment Strategy

The application is configured to be deployed in a cloud environment with auto-scaling capabilities:

- Uses Gunicorn as the WSGI server
- Configured for PostgreSQL database connection
- Environment variables for configuration management
- Static file handling for uploads and assets

The `.replit` configuration shows that the application:
- Runs on Python 3.11
- Uses Gunicorn to serve the application
- Binds to 0.0.0.0:5000 for accepting all incoming connections
- Uses port reuse for development hot reloading
- Requires OpenSSL and PostgreSQL as system dependencies

The application is designed to be containerized and deployed to a cloud environment that supports auto-scaling.

## Security Considerations

The application implements several security best practices:
- CSRF protection for all forms
- Password hashing for storing credentials
- Input validation on all user-submitted data
- Secure file upload handling with extension and size validation
- Role-based access control
- Session management

## Potential Improvements

Areas where the architecture could be extended or improved:
- API endpoints for potential mobile applications or third-party integrations
- Asynchronous task processing for email notifications and background jobs
- Caching layer for improved performance
- Full-text search for job listings
- Containerization with Docker for easier deployment