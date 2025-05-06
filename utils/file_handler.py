import os
import uuid
from flask import current_app
from werkzeug.utils import secure_filename

def allowed_file(filename, allowed_extensions=None):
    """
    Check if the uploaded file has an allowed extension
    """
    if allowed_extensions is None:
        allowed_extensions = current_app.config['ALLOWED_EXTENSIONS']
    
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_file(file, folder='uploads'):
    """
    Save an uploaded file to the specified folder
    Returns the path to the saved file
    """
    if file and allowed_file(file.filename):
        # Secure the filename and add a unique identifier
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        
        # Create the target directory if it doesn't exist
        target_dir = os.path.join(current_app.static_folder, folder)
        os.makedirs(target_dir, exist_ok=True)
        
        # Create parent directories if they don't exist
        os.makedirs(os.path.dirname(os.path.join(target_dir, unique_filename)), exist_ok=True)
        
        # Save the file
        file_path = os.path.join(target_dir, unique_filename)
        file.save(file_path)
        
        # Return the relative path for storing in the database
        return os.path.join(folder, unique_filename)
    
    return None

def delete_file(file_path):
    """
    Delete a file from the specified path
    """
    if file_path:
        full_path = os.path.join(current_app.static_folder, file_path)
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
    return False
