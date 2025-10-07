import os
import uuid
from datetime import datetime
from config import ALLOWED_RESUME_EXTENSIONS, MAX_RESUME_SIZE_MB
from database.connection import get_database
import gridfs
from bson.objectid import ObjectId

def get_gridfs():
    """Get GridFS instance"""
    db = get_database()
    if db is not None:
        return gridfs.GridFS(db)
    return None

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_RESUME_EXTENSIONS

def get_file_size_mb(file_bytes):
    """Get file size in MB"""
    return len(file_bytes) / (1024 * 1024)

def save_resume(uploaded_file, user_id):
    """
    Save uploaded resume file to MongoDB GridFS
    Returns: (success, filename/error_message)
    """
    try:
        fs = get_gridfs()
        if not fs:
            return False, "Database connection error"
        
        # Reset file pointer to beginning
        uploaded_file.seek(0)
        
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
        
        # Save to GridFS
        file_id = fs.put(
            file_bytes,
            filename=filename,
            user_id=user_id,
            upload_date=datetime.utcnow(),
            content_type=uploaded_file.type if hasattr(uploaded_file, 'type') else 'application/octet-stream'
        )
        
        # Reset file pointer again for potential re-use
        uploaded_file.seek(0)
        
        return True, filename
    
    except Exception as e:
        return False, f"Error saving file: {str(e)}"

def get_resume_data(filename):
    """Get resume file data from GridFS"""
    try:
        fs = get_gridfs()
        if not fs:
            return None
        
        file = fs.find_one({"filename": filename})
        if file:
            return file.read()
        return None
    except Exception as e:
        print(f"Error getting resume: {e}")
        return None

def resume_exists(filename):
    """Check if resume file exists in GridFS"""
    try:
        if not filename:
            return False
        fs = get_gridfs()
        if not fs:
            return False
        return fs.exists({"filename": filename})
    except Exception as e:
        print(f"Error checking resume: {e}")
        return False

def delete_resume(filename):
    """Delete resume file from GridFS"""
    try:
        if not filename:
            return False
        fs = get_gridfs()
        if not fs:
            return False
        
        file = fs.find_one({"filename": filename})
        if file:
            fs.delete(file._id)
            return True
        return False
    except Exception as e:
        print(f"Error deleting resume: {e}")
        return False

def get_resume_path(filename):
    """
    This function is kept for compatibility but returns None
    since we're using GridFS instead of file system
    """
    return None

def list_user_resumes(user_id):
    """List all resumes uploaded by a user"""
    try:
        fs = get_gridfs()
        if not fs:
            return []
        
        files = fs.find({"user_id": user_id}).sort("upload_date", -1)
        resume_list = []
        
        for file in files:
            resume_list.append({
                "filename": file.filename,
                "upload_date": file.upload_date,
                "size": file.length,
                "content_type": file.content_type
            })
        
        return resume_list
    except Exception as e:
        print(f"Error listing resumes: {e}")
        return []