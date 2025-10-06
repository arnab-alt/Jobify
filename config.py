import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Try to get from Streamlit secrets first (for cloud deployment)
# Fall back to environment variables (for local development)
def get_config(key, default=""):
    try:
        # Try Streamlit secrets (cloud deployment)
        return st.secrets.get(key, default)
    except:
        # Fall back to environment variables (local development)
        return os.getenv(key, default)

MONGODB_URI = get_config("MONGODB_URI", "mongodb://localhost:27017/")
DATABASE_NAME = get_config("DATABASE_NAME", "job_portal")
RAPIDAPI_KEY = get_config("RAPIDAPI_KEY", "")

# Resume upload settings
RESUME_UPLOAD_FOLDER = "resumes"
ALLOWED_RESUME_EXTENSIONS = {'pdf', 'doc', 'docx'}
MAX_RESUME_SIZE_MB = 5

COUNTRIES = ["USA", "UK", "India", "Canada", "Germany", "Australia", "Singapore", 
             "UAE", "Netherlands", "France", "Japan", "China", "Spain", "Italy",
             "Brazil", "Mexico", "Switzerland", "Sweden", "Norway", "Denmark"]

# Main job categories with subcategories
JOB_CATEGORIES = {
    "Software Engineering": [
        "Full Stack Developer", "Frontend Developer", "Backend Developer",
        "React Developer", "Angular Developer", "Vue.js Developer",
        "Node.js Developer", "Django Developer", "Flask Developer",
        "Java Developer", "Python Developer", "C++ Developer", "C Developer",
        ".NET Developer", "PHP Developer", "Ruby Developer", "Go Developer",
        "Mobile App Developer", "iOS Developer", "Android Developer",
        "Software Engineer", "Software Architect"
    ],
    "Data Science & Analytics": [
        "Data Scientist", "Data Analyst", "Data Engineer", "Data Entry",
        "Business Analyst", "Business Intelligence Analyst",
        "Machine Learning Engineer", "Big Data Engineer",
        "Power BI Developer", "Tableau Developer", "ETL Developer",
        "Analytics Engineer"
    ],
    "AI & Machine Learning": [
        "AI Engineer", "Machine Learning Engineer", "Deep Learning Engineer",
        "NLP Engineer", "Computer Vision Engineer", "AI Researcher",
        "MLOps Engineer", "AI/ML Specialist"
    ],
    "DevOps & Cloud": [
        "DevOps Engineer", "Cloud Engineer", "AWS Engineer", "Azure Engineer",
        "GCP Engineer", "Site Reliability Engineer", "Infrastructure Engineer",
        "Kubernetes Engineer", "Docker Specialist", "Platform Engineer",
        "Cloud Architect"
    ],
    "Design & Creative": [
        "UI/UX Designer", "Graphic Designer", "Product Designer",
        "Web Designer", "Motion Graphics Designer", "3D Designer",
        "Visual Designer", "Interaction Designer"
    ],
    "Product & Management": [
        "Product Manager", "Project Manager", "Scrum Master",
        "Program Manager", "Technical Product Manager", "Agile Coach",
        "Engineering Manager", "Technical Lead"
    ],
    "Quality & Testing": [
        "QA Engineer", "Test Engineer", "Automation Engineer",
        "SDET", "Performance Tester", "Security Tester",
        "Quality Assurance Analyst"
    ],
    "Cybersecurity": [
        "Security Engineer", "Penetration Tester", "Security Analyst",
        "SOC Analyst", "Security Architect", "Cybersecurity Consultant",
        "Information Security Specialist"
    ],
    "Database": [
        "Database Administrator", "Database Developer", "SQL Developer",
        "MongoDB Developer", "PostgreSQL Developer", "DBA"
    ],
    "Other": [
        "Technical Writer", "Sales Engineer", "Solutions Architect",
        "System Administrator", "Network Engineer", "IT Support",
        "Help Desk Technician", "Support Engineer"
    ]
}

# Flatten for search - sorted alphabetically for better UX
ALL_JOB_PROFILES = []
for category, subcategories in JOB_CATEGORIES.items():
    ALL_JOB_PROFILES.extend(subcategories)

ALL_JOB_PROFILES = sorted(list(set(ALL_JOB_PROFILES)))

# Job boards/sources
JOB_SOURCES = ["LinkedIn", "Indeed", "Glassdoor", "Monster", "Dice", "JSearch", 
               "ZipRecruiter", "CareerBuilder"]

# Pagination settings
JOBS_PER_PAGE = 50