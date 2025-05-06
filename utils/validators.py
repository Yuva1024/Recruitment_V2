import re
from flask_wtf.file import FileAllowed
from wtforms.validators import ValidationError

def validate_phone_number(form, field):
    """
    Validate that the field contains a valid phone number
    """
    if field.data:
        pattern = re.compile(r'^\+?[\d\s\-().]{7,20}$')
        if not pattern.match(field.data):
            raise ValidationError('Invalid phone number format.')

def validate_website(form, field):
    """
    Validate that the field contains a valid website URL
    """
    if field.data:
        pattern = re.compile(
            r'^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?'
            r'[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$'
        )
        if not pattern.match(field.data):
            raise ValidationError('Invalid website URL format.')

def validate_password_strength(form, field):
    """
    Validate that the password meets minimum strength requirements
    """
    if field.data:
        if len(field.data) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        
        if not any(char.isdigit() for char in field.data):
            raise ValidationError('Password must contain at least one number.')
        
        if not any(char.isupper() for char in field.data):
            raise ValidationError('Password must contain at least one uppercase letter.')
        
        if not any(char.islower() for char in field.data):
            raise ValidationError('Password must contain at least one lowercase letter.')

def validate_file_size(max_size_mb=5):
    """
    Create a validator that checks if the file size is within limits
    """
    def _validate_file_size(form, field):
        if field.data:
            # Check file size
            file_size_bytes = len(field.data.read())
            field.data.seek(0)  # Reset file pointer
            
            max_size_bytes = max_size_mb * 1024 * 1024
            
            if file_size_bytes > max_size_bytes:
                raise ValidationError(f'File size exceeds the maximum limit of {max_size_mb}MB.')
    
    return _validate_file_size

def create_file_validator(allowed_extensions, max_size_mb=5):
    """
    Create a combined validator for files (extensions and size)
    """
    return [
        FileAllowed(allowed_extensions, f'Only {", ".join(allowed_extensions)} files are allowed.'),
        validate_file_size(max_size_mb)
    ]
