from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, TextAreaField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from utils.validators import validate_phone_number, validate_website, create_file_validator

class CandidateProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    phone = StringField('Phone Number', validators=[Optional(), validate_phone_number])
    address = StringField('Address', validators=[Optional(), Length(max=200)])
    professional_title = StringField('Professional Title', validators=[Optional(), Length(max=100)])
    summary = TextAreaField('Professional Summary', validators=[Optional()])
    skills = TextAreaField('Skills', validators=[Optional()])
    experience = TextAreaField('Work Experience', validators=[Optional()])
    education = TextAreaField('Education', validators=[Optional()])
    resume = FileField('Resume/CV', validators=create_file_validator(['pdf', 'doc', 'docx', 'txt']))
    submit = SubmitField('Save Profile')

class EmployerProfileForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired(), Length(max=100)])
    company_website = StringField('Company Website', validators=[Optional(), validate_website, Length(max=255)])
    company_description = TextAreaField('Company Description', validators=[DataRequired()])
    industry = StringField('Industry', validators=[DataRequired(), Length(max=100)])
    company_size = SelectField('Company Size', choices=[
        ('1-10', '1-10 employees'),
        ('11-50', '11-50 employees'),
        ('51-200', '51-200 employees'),
        ('201-500', '201-500 employees'),
        ('501-1000', '501-1000 employees'),
        ('1001+', '1001+ employees')
    ], validators=[DataRequired()])
    founded_year = IntegerField('Founded Year', validators=[Optional(), NumberRange(min=1800, max=2100)])
    location = StringField('Company Location', validators=[DataRequired(), Length(max=100)])
    contact_email = StringField('Contact Email', validators=[DataRequired(), Length(max=120)])
    contact_phone = StringField('Contact Phone', validators=[Optional(), validate_phone_number])
    logo = FileField('Company Logo', validators=create_file_validator(['jpg', 'jpeg', 'png', 'gif']))
    submit = SubmitField('Save Profile')
