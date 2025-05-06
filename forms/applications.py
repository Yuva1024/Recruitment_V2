from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import TextAreaField, SubmitField
from wtforms.validators import Optional
from utils.validators import create_file_validator

class JobApplicationForm(FlaskForm):
    cover_letter = TextAreaField('Cover Letter', validators=[Optional()])
    resume = FileField('Resume/CV', validators=create_file_validator(['pdf', 'doc', 'docx', 'txt']))
    submit = SubmitField('Submit Application')

class ApplicationStatusForm(FlaskForm):
    status = TextAreaField('Status Update Notes', validators=[Optional()])
    submit = SubmitField('Update Status')
