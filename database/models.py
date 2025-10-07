# from datetime import datetime
# from bson import ObjectId

# class User:
#     """User model"""
#     @staticmethod
#     def create(email, password_hash, name, role):
#         return {
#             "email": email,
#             "password_hash": password_hash,
#             "name": name,
#             "role": role,
#             "created_at": datetime.utcnow(),
#             # Profile fields
#             "phone": "",
#             "location": "",
#             "bio": "",
#             "skills": [],
#             "experience": "",
#             "education": "",
#             "resume_url": "",
#             "linkedin_url": "",
#             "github_url": "",
#             "portfolio_url": "",
#             # Recruiter specific
#             "company": "",
#             "company_website": "",
#             "company_size": ""
#         }
    
#     @staticmethod
#     def find_by_email(users_collection, email):
#         return users_collection.find_one({"email": email})
    
#     @staticmethod
#     def find_by_id(users_collection, user_id):
#         return users_collection.find_one({"_id": ObjectId(user_id)})
    
#     @staticmethod
#     def update_profile(users_collection, user_id, profile_data):
#         return users_collection.update_one(
#             {"_id": ObjectId(user_id)},
#             {"$set": profile_data}
#         )

# class Job:
#     """Job model"""
#     @staticmethod
#     def create(recruiter_id, title, company, location, description, category, subcategory, 
#                salary_min, salary_max, employment_type, experience_level, skills_required):
#         return {
#             "recruiter_id": recruiter_id,
#             "title": title,
#             "company": company,
#             "location": location,
#             "description": description,
#             "category": category,
#             "subcategory": subcategory,
#             "salary_min": salary_min,
#             "salary_max": salary_max,
#             "employment_type": employment_type,
#             "experience_level": experience_level,
#             "skills_required": skills_required,
#             "status": "active",
#             "created_at": datetime.utcnow(),
#             "views": 0,
#             "applications_count": 0
#         }
    
#     @staticmethod
#     def find_by_recruiter(jobs_collection, recruiter_id):
#         return list(jobs_collection.find({"recruiter_id": recruiter_id}).sort("created_at", -1))
    
#     @staticmethod
#     def find_all_active(jobs_collection):
#         return list(jobs_collection.find({"status": "active"}).sort("created_at", -1))
    
#     @staticmethod
#     def find_by_id(jobs_collection, job_id):
#         return jobs_collection.find_one({"_id": ObjectId(job_id)})
    
#     @staticmethod
#     def increment_views(jobs_collection, job_id):
#         jobs_collection.update_one(
#             {"_id": ObjectId(job_id)},
#             {"$inc": {"views": 1}}
#         )
    
#     @staticmethod
#     def increment_applications(jobs_collection, job_id):
#         jobs_collection.update_one(
#             {"_id": ObjectId(job_id)},
#             {"$inc": {"applications_count": 1}}
#         )

# class Application:
#     """Application model"""
#     @staticmethod
#     def create(job_id, user_id, user_name, user_email, resume_filename=None):
#         return {
#             "job_id": job_id,
#             "user_id": user_id,
#             "user_name": user_name,
#             "user_email": user_email,
#             "resume_filename": resume_filename,  # NEW FIELD
#             "status": "pending",
#             "applied_at": datetime.utcnow()
#         }
    
#     @staticmethod
#     def find_by_job(applications_collection, job_id):
#         return list(applications_collection.find({"job_id": job_id}).sort("applied_at", -1))
    
#     @staticmethod
#     def find_by_user(applications_collection, user_id):
#         return list(applications_collection.find({"user_id": user_id}).sort("applied_at", -1))

from datetime import datetime
from bson import ObjectId

class User:
    """User model"""
    @staticmethod
    def create(email, password_hash, name, role):
        return {
            "email": email,
            "password_hash": password_hash,
            "name": name,
            "role": role,
            "created_at": datetime.utcnow(),
            # Profile fields
            "phone": "",
            "location": "",
            "bio": "",
            "skills": [],
            "experience": "",
            "education": "",
            "resume_url": "",
            "linkedin_url": "",
            "github_url": "",
            "portfolio_url": "",
            # Recruiter specific
            "company": "",
            "company_website": "",
            "company_size": ""
        }
    
    @staticmethod
    def find_by_email(users_collection, email):
        return users_collection.find_one({"email": email})
    
    @staticmethod
    def find_by_id(users_collection, user_id):
        return users_collection.find_one({"_id": ObjectId(user_id)})
    
    @staticmethod
    def update_profile(users_collection, user_id, profile_data):
        return users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": profile_data}
        )

class Job:
    """Job model"""
    @staticmethod
    def create(recruiter_id, title, company, location, description, category, subcategory, 
               salary_min, salary_max, employment_type, experience_level, skills_required):
        return {
            "recruiter_id": recruiter_id,
            "title": title,
            "company": company,
            "location": location,
            "description": description,
            "category": category,
            "subcategory": subcategory,
            "salary_min": salary_min,
            "salary_max": salary_max,
            "employment_type": employment_type,
            "experience_level": experience_level,
            "skills_required": skills_required,
            "status": "active",
            "created_at": datetime.utcnow(),
            "views": 0,
            "applications_count": 0
        }
    
    @staticmethod
    def find_by_recruiter(jobs_collection, recruiter_id):
        return list(jobs_collection.find({"recruiter_id": recruiter_id}).sort("created_at", -1))
    
    @staticmethod
    def find_all_active(jobs_collection):
        return list(jobs_collection.find({"status": "active"}).sort("created_at", -1))
    
    @staticmethod
    def find_by_id(jobs_collection, job_id):
        try:
            if isinstance(job_id, str):
                return jobs_collection.find_one({"_id": ObjectId(job_id)})
            return jobs_collection.find_one({"_id": job_id})
        except Exception as e:
            print(f"Error finding job: {e}")
            return None
    
    @staticmethod
    def increment_views(jobs_collection, job_id):
        try:
            if isinstance(job_id, str):
                job_id = ObjectId(job_id)
            jobs_collection.update_one(
                {"_id": job_id},
                {"$inc": {"views": 1}}
            )
        except Exception as e:
            print(f"Error incrementing views: {e}")
    
    @staticmethod
    def increment_applications(jobs_collection, job_id):
        try:
            if isinstance(job_id, str):
                job_id = ObjectId(job_id)
            jobs_collection.update_one(
                {"_id": job_id},
                {"$inc": {"applications_count": 1}}
            )
        except Exception as e:
            print(f"Error incrementing applications: {e}")

class Application:
    """Application model"""
    @staticmethod
    def create(applications_collection, user_id, job_id, resume_filename, user_name, user_email):
        """Create a new application"""
        try:
            # Convert job_id to ObjectId if it's a string
            if isinstance(job_id, str):
                job_id = ObjectId(job_id)
            
            application_data = {
                "job_id": str(job_id),  # Store as string for easier querying
                "user_id": user_id,
                "user_name": user_name,
                "user_email": user_email,
                "resume_filename": resume_filename,
                "status": "pending",
                "applied_at": datetime.utcnow()
            }
            
            result = applications_collection.insert_one(application_data)
            
            if result.inserted_id:
                # Increment job applications count
                from database.connection import get_collection
                jobs_collection = get_collection("jobs")
                Job.increment_applications(jobs_collection, job_id)
                return application_data
            return None
        except Exception as e:
            print(f"Error creating application: {e}")
            return None
    
    @staticmethod
    def find_by_job(applications_collection, job_id):
        """Find all applications for a job"""
        try:
            if isinstance(job_id, ObjectId):
                job_id = str(job_id)
            return list(applications_collection.find({"job_id": job_id}).sort("applied_at", -1))
        except Exception as e:
            print(f"Error finding applications by job: {e}")
            return []
    
    @staticmethod
    def find_by_user(applications_collection, user_id):
        """Find all applications by a user"""
        try:
            return list(applications_collection.find({"user_id": user_id}).sort("applied_at", -1))
        except Exception as e:
            print(f"Error finding applications by user: {e}")
            return []
    
    @staticmethod
    def find_by_user_and_job(applications_collection, user_id, job_id):
        """Check if user already applied for a job"""
        try:
            if isinstance(job_id, ObjectId):
                job_id = str(job_id)
            return applications_collection.find_one({
                "user_id": user_id,
                "job_id": job_id
            })
        except Exception as e:
            print(f"Error checking existing application: {e}")
            return None