from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, BooleanField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class JobSearchForm(FlaskForm):
    keyword = StringField('Keywords', validators=[Optional()])
    location = StringField('Location', validators=[Optional()])
    job_type = SelectField('Job Type', choices=[
        ('', 'All Types'),
        ('full-time', 'Full Time'),
        ('part-time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('temporary', 'Temporary')
    ], validators=[Optional()])
    experience_level = SelectField('Experience Level', choices=[
        ('', 'All Levels'),
        ('entry', 'Entry Level'),
        ('mid', 'Mid Level'),
        ('senior', 'Senior Level'),
        ('executive', 'Executive')
    ], validators=[Optional()])
    remote = BooleanField('Remote Jobs Only', default=False)
    submit = SubmitField('Search')

class JobPostForm(FlaskForm):
    title = StringField('Job Title', validators=[DataRequired(), Length(max=100)])
    company = StringField('Company Name', validators=[DataRequired(), Length(max=100)])
    location = StringField('Location', validators=[DataRequired(), Length(max=100)])
    job_type = SelectField('Job Type', choices=[
        ('full-time', 'Full Time'),
        ('part-time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('temporary', 'Temporary')
    ], validators=[DataRequired()])
    experience_level = SelectField('Experience Level', choices=[
        ('entry', 'Entry Level'),
        ('mid', 'Mid Level'),
        ('senior', 'Senior Level'),
        ('executive', 'Executive')
    ], validators=[DataRequired()])
    education_level = SelectField('Education Level', choices=[
        ('high-school', 'High School'),
        ('associate', 'Associate Degree'),
        ('bachelor', 'Bachelor\'s Degree'),
        ('master', 'Master\'s Degree'),
        ('doctorate', 'Doctorate')
    ], validators=[DataRequired()])
    industry = StringField('Industry', validators=[DataRequired(), Length(max=100)])
    salary_range = StringField('Salary Range', validators=[Optional(), Length(max=50)])
    description = TextAreaField('Job Description', validators=[DataRequired()])
    requirements = TextAreaField('Requirements', validators=[DataRequired()])
    is_remote = BooleanField('Remote Job', default=False)
    closing_date = DateField('Closing Date', validators=[Optional()], format='%Y-%m-%d')
    submit = SubmitField('Post Job')
