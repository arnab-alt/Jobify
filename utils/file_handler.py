import os
import uuid
from datetime import datetime
from config import RESUME_UPLOAD_FOLDER, ALLOWED_RESUME_EXTENSIONS, MAX_RESUME_SIZE_MB

def create_resume_folder():
    """Create resumes folder if it doesn't exist"""
    if not os.path.exists(RESUME_UPLOAD_FOLDER):
        os.makedirs(RESUME_UPLOAD_FOLDER)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_RESUME_EXTENSIONS

def get_file_size_mb(file_bytes):
    """Get file size in MB"""
    return len(file_bytes) / (1024 * 1024)

def save_resume(uploaded_file, user_id):
    """
    Save uploaded resume file
    Returns: (success, filename/error_message)
    """
    try:
        create_resume_folder()
        
        # Check if file is allowed
        if not allowed_file(uploaded_file.name):
            return False, f"File type not allowed. Allowed types: {', '.join(ALLOWED_RESUME_EXTENSIONS)}"
        
        # Read file bytes
        file_bytes = uploaded_file.read()
        
        # Check file size
        file_size_mb = get_file_size_mb(file_bytes)
        if file_size_mb > MAX_RESUME_SIZE_MB:
            return False, f"File size exceeds {MAX_RESUME_SIZE_MB}MB limit"
        
        # Generate unique filename
        file_extension = uploaded_file.name.rsplit('.', 1)[1].lower()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        filename = f"resume_{user_id}_{timestamp}_{unique_id}.{file_extension}"
        
        # Save file
        filepath = os.path.join(RESUME_UPLOAD_FOLDER, filename)
        with open(filepath, 'wb') as f:
            f.write(file_bytes)
        
        return True, filename
    
    except Exception as e:
        return False, f"Error saving file: {str(e)}"

def get_resume_path(filename):
    """Get full path to resume file"""
    if not filename:
        return None
    return os.path.join(RESUME_UPLOAD_FOLDER, filename)

def resume_exists(filename):
    """Check if resume file exists"""
    if not filename:
        return False
    filepath = get_resume_path(filename)
    return os.path.exists(filepath)

def delete_resume(filename):
    """Delete resume file"""
    try:
        if filename and resume_exists(filename):
            filepath = get_resume_path(filename)
            os.remove(filepath)
            return True
        return False
    except Exception as e:
        print(f"Error deleting resume: {e}")
        return False