import streamlit as st
from database.connection import get_collection
from database.models import Job, Application
from config import JOB_CATEGORIES, COUNTRIES
from bson import ObjectId
from utils.file_handler import get_resume_data, resume_exists
import time

# Modern, enhanced CSS matching user dashboard style
st.markdown("""
    <style>
        /* Global Styles */
        * {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
        }
        
        .dashboard-card {
            background: white;
            border: 1px solid #d6d6d6;
            border-radius: 8px;
            padding: 18px;
            margin-bottom: 16px;
            transition: all 0.2s ease;
        }
        
        .dashboard-card:hover {
            box-shadow: 0 2px 16px rgba(0, 0, 0, 0.1);
            border-color: #b0b0b0;
        }
        
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            padding: 24px;
            text-align: center;
            transition: all 0.3s ease;
            border: none;
        }
        
        .metric-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
        }
        
        .metric-value {
            font-size: 36px;
            font-weight: 700;
            color: white;
            margin: 8px 0;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .metric-label {
            font-size: 12px;
            color: rgba(255,255,255,0.95);
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        /* Job Item Card - Enhanced */
        .job-item {
            background: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 16px;
            margin: 12px 0;
            border-left: 4px solid #667eea;
            transition: all 0.2s ease;
            position: relative;
        }
        
        .job-item:hover {
            box-shadow: 0 2px 16px rgba(0, 0, 0, 0.1);
            border-left-color: #764ba2;
            transform: translateX(4px);
        }
        
        .job-item-title {
            font-size: 18px;
            font-weight: 600;
            color: #333;
            margin-bottom: 4px;
            line-height: 1.3;
        }
        
        .job-item-company {
            font-size: 14px;
            font-weight: 400;
            color: #666;
            margin-bottom: 4px;
        }
        
        .job-item-meta {
            color: #666;
            font-size: 14px;
            font-weight: 400;
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
            margin-top: 4px;
        }
        
        .meta-separator {
            color: #ccc;
        }
        
        /* Job Details Section */
        .job-details-row {
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin: 8px 0;
            padding: 8px 0;
            border-top: 1px solid #f0f0f0;
            border-bottom: 1px solid #f0f0f0;
        }
        
        .job-detail-item {
            display: flex;
            align-items: center;
            gap: 4px;
            font-size: 13px;
            color: #666;
        }
        
        .detail-icon {
            font-size: 13px;
            color: #888;
        }
        
        /* Applicant Item Card */
        .applicant-item {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 14px 16px;
            margin: 10px 0;
            transition: all 0.2s ease;
        }
        
        .applicant-item:hover {
            border-color: #667eea;
            box-shadow: 0 2px 12px rgba(102, 126, 234, 0.1);
            transform: translateY(-2px);
        }
        
        .applicant-name {
            font-size: 16px;
            font-weight: 600;
            color: #333;
            margin-bottom: 4px;
        }
        
        .applicant-email {
            color: #667eea;
            font-size: 14px;
            margin-bottom: 4px;
            font-weight: 500;
        }
        
        .applicant-date {
            color: #888;
            font-size: 12px;
        }
        
        .status-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .status-active {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
        }
        
        .status-closed {
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            color: white;
            box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
        }
        
        .status-pending {
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            color: white;
            box-shadow: 0 2px 8px rgba(245, 158, 11, 0.3);
        }
        
        .status-accepted {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
        }
        
        .status-rejected {
            background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
            color: white;
            box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
        }
        
        .section-header {
            font-size: 28px;
            font-weight: 700;
            color: #1a1a1a;
            margin: 24px 0 20px 0;
            padding-bottom: 12px;
            border-bottom: 3px solid #667eea;
        }
        
        .section-subheader {
            font-size: 20px;
            font-weight: 700;
            color: #333;
            margin: 16px 0 12px 0;
            padding-bottom: 8px;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .info-box {
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            border-left: 4px solid #3b82f6;
            border-radius: 8px;
            padding: 16px;
            margin: 16px 0;
        }
        
        .stat-value {
            font-size: 24px;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .stat-label {
            font-size: 11px;
            color: #888;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 4px;
        }
        
        /* Filter Section */
        .filter-section {
            background: #ffffff;
            padding: 16px;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
            margin-bottom: 16px;
        }
        
        /* Form Section */
        .form-section {
            background: #ffffff;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
        }
        
        /* Divider */
        .divider {
            height: 1px;
            background: #e0e0e0;
            margin: 12px 0;
        }
        
        /* Button enhancements */
        .stButton > button {
            border-radius: 6px;
            font-weight: 500;
            font-size: 14px;
            padding: 8px 16px;
            transition: all 0.2s ease;
        }
        
        /* Custom badges */
        .badge {
            display: inline-block;
            padding: 4px 12px;
            background: #e8f4fd;
            color: #0066cc;
            border: 1px solid #d0e7f9;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            margin: 2px;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .job-details-row {
                flex-direction: column;
                gap: 8px;
            }
        }
    </style>
""", unsafe_allow_html=True)

def show_recruiter_dashboard(user):
    st.title("💼 Recruiter Dashboard")
    st.caption("Manage your job postings and applications")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Initialize active_tab in session state if not exists
    if 'active_recruiter_tab' not in st.session_state:
        st.session_state.active_recruiter_tab = 0
    
    # Tab-based navigation
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "✏️ Post New Job", "📋 Manage Jobs"])
    
    with tab1:
        show_overview(user)
    
    with tab2:
        show_post_job(user)
    
    with tab3:
        show_manage_jobs(user)

def show_overview(user):
    st.markdown("## Dashboard Overview")
    st.markdown("<br>", unsafe_allow_html=True)
    
    try:
        jobs_collection = get_collection("jobs")
        my_jobs = Job.find_by_recruiter(jobs_collection, str(user['_id']))
        
        total_jobs = len(my_jobs)
        active_jobs = len([j for j in my_jobs if j['status'] == 'active'])
        total_views = sum(j.get('views', 0) for j in my_jobs)
        total_applications = sum(j.get('applications_count', 0) for j in my_jobs)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Total Jobs</div>
                    <div class="metric-value">{total_jobs}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Active Jobs</div>
                    <div class="metric-value">{active_jobs}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Total Views</div>
                    <div class="metric-value">{total_views}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Applications</div>
                    <div class="metric-value">{total_applications}</div>
                </div>
            """, unsafe_allow_html=True)
        
        if my_jobs:
            st.markdown("### Recent Job Postings")
            st.markdown("<br>", unsafe_allow_html=True)
            
            for job in my_jobs[:5]:
                st.markdown('<div class="job-item">', unsafe_allow_html=True)
                
                # Status badge in top right
                status_class = "status-active" if job['status'] == 'active' else "status-closed"
                status_text = "Active" if job['status'] == 'active' else "Closed"
                st.markdown(f'<div style="position: absolute; top: 12px; right: 12px;"><span class="status-badge {status_class}">{status_text}</span></div>', unsafe_allow_html=True)
                
                # Title
                st.markdown(f'<div class="job-item-title">{job["title"]}</div>', unsafe_allow_html=True)
                
                # Company and location
                st.markdown(f'''
                    <div class="job-item-meta">
                        <span>🏢 {job["company"]}</span>
                        <span class="meta-separator">•</span>
                        <span>📍 {job["location"]}</span>
                        <span class="meta-separator">•</span>
                        <span>{job["category"]}</span>
                    </div>
                ''', unsafe_allow_html=True)
                
                # Stats row
                st.markdown('<div class="job-details-row">', unsafe_allow_html=True)
                st.markdown(f'''
                    <div class="job-detail-item">
                        <span class="detail-icon">👁️</span>
                        <span><strong>{job.get('views', 0)}</strong> views</span>
                    </div>
                    <div class="job-detail-item">
                        <span class="detail-icon">📋</span>
                        <span><strong>{job.get('applications_count', 0)}</strong> applications</span>
                    </div>
                    <div class="job-detail-item">
                        <span class="detail-icon">⏰</span>
                        <span>{job.get('employment_type', 'N/A')}</span>
                    </div>
                    <div class="job-detail-item">
                        <span class="detail-icon">💰</span>
                        <span>${job.get('salary_min', 0)//1000}K - ${job.get('salary_max', 0)//1000}K</span>
                    </div>
                ''', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.info("📝 No jobs posted yet. Click 'Post New Job' to get started!")
            st.markdown('</div>', unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"❌ Error loading overview: {str(e)}")

def show_post_job(user):
    st.markdown("## Post a New Job")
    st.caption("Fill in the details to create a job listing")
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    
    with st.form("post_job_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Job Title *", placeholder="e.g., Senior React Developer")
            company = st.text_input("Company Name *", value=user.get('company', user.get('name', '')))
            location = st.selectbox("Location *", COUNTRIES)
        
        with col2:
            category = st.selectbox("Job Category *", list(JOB_CATEGORIES.keys()))
            subcategory = st.selectbox("Job Role/Subcategory *", JOB_CATEGORIES[category])
            employment_type = st.selectbox("Employment Type *", 
                                          ["Full-time", "Part-time", "Contract", "Internship"])
        
        col3, col4 = st.columns(2)
        
        with col3:
            salary_min = st.number_input("Minimum Salary (USD/year)", min_value=0, value=50000, step=5000)
            experience_level = st.selectbox("Experience Level *", 
                                          ["Entry Level", "Mid Level", "Senior Level", "Lead/Principal"])
        
        with col4:
            salary_max = st.number_input("Maximum Salary (USD/year)", min_value=0, value=100000, step=5000)
        
        skills_input = st.text_input("Required Skills (comma-separated) *", 
                                    placeholder="React, JavaScript, Node.js, MongoDB")
        
        description = st.text_area("Job Description *", height=180, 
                                   placeholder="Describe the role, requirements, responsibilities, and benefits...")
        
        st.caption("* Required fields")
        st.markdown("<br>", unsafe_allow_html=True)
        
        submitted = st.form_submit_button("📤 Post Job", type="primary", use_container_width=True)
        
        if submitted:
            if not all([title, company, location, category, subcategory, description, skills_input]):
                st.error("❌ Please fill all required fields")
            elif not title.strip() or not company.strip() or not description.strip():
                st.error("❌ Title, Company, and Description cannot be empty")
            elif salary_min >= salary_max:
                st.error("❌ Maximum salary must be greater than minimum salary")
            elif salary_min < 0 or salary_max < 0:
                st.error("❌ Salaries cannot be negative")
            else:
                try:
                    skills_required = [s.strip() for s in skills_input.split(',') if s.strip()]
                    
                    if not skills_required:
                        st.error("❌ Please enter at least one skill")
                    else:
                        jobs_collection = get_collection("jobs")
                        job_data = Job.create(
                            str(user['_id']),
                            title.strip(),
                            company.strip(),
                            location,
                            description.strip(),
                            category,
                            subcategory,
                            salary_min,
                            salary_max,
                            employment_type,
                            experience_level,
                            skills_required
                        )
                        
                        result = jobs_collection.insert_one(job_data)
                        
                        if result.inserted_id:
                            st.success("✅ Job posted successfully!")
                            # Clear form and switch to Manage Jobs tab
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error("❌ Failed to post job")
                            
                except Exception as e:
                    st.error(f"❌ Error posting job: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_manage_jobs(user):
    st.markdown("## Manage Jobs & Applications")
    st.markdown("<br>", unsafe_allow_html=True)
    
    try:
        jobs_collection = get_collection("jobs")
        my_jobs = Job.find_by_recruiter(jobs_collection, str(user['_id']))
        
        if not my_jobs:
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.info("📝 No jobs posted yet. Go to 'Post New Job' to create your first job posting!")
            st.markdown('</div>', unsafe_allow_html=True)
            return
        
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            filter_status = st.selectbox("🔍 Filter by Status", ["All", "Active", "Closed"])
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        filtered_jobs = my_jobs
        if filter_status == "Active":
            filtered_jobs = [j for j in my_jobs if j['status'] == 'active']
        elif filter_status == "Closed":
            filtered_jobs = [j for j in my_jobs if j['status'] != 'active']
        
        st.write(f"**{len(filtered_jobs)} jobs found**")
        st.markdown("<br>", unsafe_allow_html=True)
        
        for job in filtered_jobs:
            job_id = str(job['_id'])
            
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            
            # Job header with status badge
            col_title, col_status = st.columns([4, 1])
            
            with col_title:
                st.markdown(f'<div class="job-item-title">{job["title"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="job-item-meta">🏢 {job["company"]}</div>', unsafe_allow_html=True)
            
            with col_status:
                if job['status'] == 'active':
                    st.markdown('<span class="status-badge status-active">✓ Active</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="status-badge status-closed">✕ Closed</span>', unsafe_allow_html=True)
            
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            
            # Job details in compact row format
            st.markdown('<div class="job-details-row">', unsafe_allow_html=True)
            st.markdown(f'''
                <div class="job-detail-item">
                    <span class="detail-icon">📍</span>
                    <span>{job['location']}</span>
                </div>
                <div class="job-detail-item">
                    <span class="detail-icon">📂</span>
                    <span>{job['category']} - {job['subcategory']}</span>
                </div>
                <div class="job-detail-item">
                    <span class="detail-icon">⏰</span>
                    <span>{job.get('employment_type', 'N/A')}</span>
                </div>
                <div class="job-detail-item">
                    <span class="detail-icon">📅</span>
                    <span>{job.get('experience_level', 'N/A')}</span>
                </div>
                <div class="job-detail-item">
                    <span class="detail-icon">💰</span>
                    <span>${job.get('salary_min', 0):,} - ${job.get('salary_max', 0):,}</span>
                </div>
                <div class="job-detail-item">
                    <span class="detail-icon">👁️</span>
                    <span><strong>{job.get('views', 0)}</strong> views</span>
                </div>
                <div class="job-detail-item">
                    <span class="detail-icon">📋</span>
                    <span><strong>{job.get('applications_count', 0)}</strong> applications</span>
                </div>
            ''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            with st.expander("👁️ View Full Details & Manage", expanded=False):
                st.markdown("**Description:**")
                st.write(job['description'])
                
                if job.get('skills_required'):
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("**All Required Skills:**")
                    st.write(", ".join(job['skills_required']))
                
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                
                col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])
                
                with col_btn1:
                    if job['status'] == 'active':
                        if st.button("🔒 Close Job", key=f"close_{job_id}", use_container_width=True):
                            try:
                                jobs_collection.update_one(
                                    {"_id": job['_id']},
                                    {"$set": {"status": "closed"}}
                                )
                                st.success("✅ Job closed")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Error closing job: {str(e)}")
                
                with col_btn2:
                    if st.button("🗑️ Delete", key=f"delete_{job_id}", use_container_width=True):
                        try:
                            # Delete the job
                            jobs_collection.delete_one({"_id": job['_id']})
                            
                            # Also delete all applications for this job
                            apps_collection = get_collection("applications")
                            apps_collection.delete_many({"job_id": job_id})
                            
                            st.success("✅ Job deleted successfully")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error deleting job: {str(e)}")
            
            # Display applications
            apps_collection = get_collection("applications")
            applications = Application.find_by_job(apps_collection, job_id)
            
            if applications:
                st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
                st.markdown(f"### Applications ({len(applications)})")
                st.markdown("<br>", unsafe_allow_html=True)
                
                for app in applications:
                    st.markdown('<div class="applicant-item">', unsafe_allow_html=True)
                    
                    col_app1, col_app2, col_app3, col_app4 = st.columns([2, 1, 1, 1])
                    
                    with col_app1:
                        st.markdown(f'<div class="applicant-name">{app["user_name"]}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="applicant-email">✉️ {app["user_email"]}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="applicant-date">📅 Applied: {app["applied_at"].strftime("%b %d, %Y at %I:%M %p")}</div>', unsafe_allow_html=True)
                    
                    with col_app2:
                        status = app['status']
                        if status == 'pending':
                            st.markdown('<span class="status-badge status-pending">⏳ Pending</span>', unsafe_allow_html=True)
                        elif status == 'accepted':
                            st.markdown('<span class="status-badge status-accepted">✓ Accepted</span>', unsafe_allow_html=True)
                        else:
                            st.markdown('<span class="status-badge status-rejected">✕ Rejected</span>', unsafe_allow_html=True)
                    
                    with col_app3:
                        if app.get('resume_filename'):
                            try:
                                if resume_exists(app['resume_filename']):
                                    resume_data = get_resume_data(app['resume_filename'])
                                    
                                    if resume_data:
                                        file_extension = app['resume_filename'].split('.')[-1]
                                        st.download_button(
                                            label="📎 Resume",
                                            data=resume_data,
                                            file_name=f"{app['user_name']}_resume.{file_extension}",
                                            mime="application/octet-stream",
                                            key=f"download_{app['_id']}",
                                            use_container_width=True
                                        )
                                    else:
                                        st.caption("Resume not found")
                                else:
                                    st.caption("Resume not found")
                            except Exception as e:
                                st.caption(f"Error: {str(e)}")
                        else:
                            st.caption("No resume")
                    
                    with col_app4:
                        if app['status'] == 'pending':
                            col_a, col_b = st.columns(2)
                            with col_a:
                                if st.button("✓", key=f"accept_{app['_id']}", help="Accept", use_container_width=True):
                                    try:
                                        apps_collection.update_one(
                                            {"_id": app['_id']},
                                            {"$set": {"status": "accepted"}}
                                        )
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"Error: {str(e)}")
                            
                            with col_b:
                                if st.button("✗", key=f"reject_{app['_id']}", help="Reject", use_container_width=True):
                                    try:
                                        apps_collection.update_one(
                                            {"_id": app['_id']},
                                            {"$set": {"status": "rejected"}}
                                        )
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"Error: {str(e)}")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"❌ Error loading jobs: {str(e)}")