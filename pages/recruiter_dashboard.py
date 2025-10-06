import streamlit as st
from database.connection import get_collection
from database.models import Job, Application
from config import JOB_CATEGORIES, COUNTRIES
from bson import ObjectId
from utils.file_handler import get_resume_data, resume_exists

# Enhanced professional CSS
st.markdown("""
    <style>
        .dashboard-card {
            background: white;
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            margin-bottom: 1.5rem;
            transition: all 0.3s ease;
        }
        
        .dashboard-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        }
        
        .metric-card {
            background: white;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            padding: 1.75rem;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            border-color: #3b82f6;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
        }
        
        .metric-value {
            font-size: 2.5rem;
            font-weight: 800;
            color: #0f172a;
            margin: 0.5rem 0;
        }
        
        .metric-label {
            font-size: 0.95rem;
            color: #64748b;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .job-item {
            background: #f8fafc;
            border-radius: 10px;
            padding: 1.25rem;
            margin: 1rem 0;
            border-left: 4px solid #3b82f6;
            transition: all 0.2s ease;
        }
        
        .job-item:hover {
            background: #f1f5f9;
            border-left-color: #2563eb;
            transform: translateX(3px);
        }
        
        .job-item-title {
            font-size: 1.1rem;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 0.5rem;
        }
        
        .job-item-meta {
            color: #64748b;
            font-size: 0.9rem;
        }
        
        .applicant-item {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 1.25rem;
            margin: 0.75rem 0;
            transition: all 0.2s ease;
        }
        
        .applicant-item:hover {
            border-color: #3b82f6;
            box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1);
        }
        
        .applicant-name {
            font-size: 1.05rem;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 0.25rem;
        }
        
        .applicant-email {
            color: #3b82f6;
            font-size: 0.9rem;
            margin-bottom: 0.25rem;
        }
        
        .applicant-date {
            color: #64748b;
            font-size: 0.85rem;
        }
        
        .status-badge {
            display: inline-block;
            padding: 0.4rem 1rem;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .status-active {
            background: #d1fae5;
            color: #065f46;
        }
        
        .status-closed {
            background: #fee2e2;
            color: #991b1b;
        }
        
        .status-pending {
            background: #fef3c7;
            color: #92400e;
        }
        
        .status-accepted {
            background: #d1fae5;
            color: #065f46;
        }
        
        .status-rejected {
            background: #fee2e2;
            color: #991b1b;
        }
        
        .section-header {
            font-size: 1.5rem;
            font-weight: 700;
            color: #0f172a;
            margin: 2rem 0 1rem 0;
            padding-bottom: 0.75rem;
            border-bottom: 2px solid #e2e8f0;
        }
        
        .info-box {
            background: #f8fafc;
            border-left: 4px solid #3b82f6;
            border-radius: 8px;
            padding: 1rem 1.25rem;
            margin: 1rem 0;
        }
        
        .job-stats {
            display: flex;
            gap: 2rem;
            margin: 1rem 0;
        }
        
        .stat-item {
            text-align: center;
        }
        
        .stat-value {
            font-size: 1.75rem;
            font-weight: 700;
            color: #3b82f6;
        }
        
        .stat-label {
            font-size: 0.85rem;
            color: #64748b;
            font-weight: 500;
        }
    </style>
""", unsafe_allow_html=True)

def show_recruiter_dashboard(user):
    st.markdown("# Recruiter Dashboard")
    st.caption("Manage your job postings and applications")
    st.markdown("<br>", unsafe_allow_html=True)
    
    view = st.radio("", ["Overview", "Post New Job", "Manage Jobs"], 
                    horizontal=True, label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if view == "Overview":
        show_overview(user)
    elif view == "Post New Job":
        show_post_job(user)
    else:
        show_manage_jobs(user)

def show_overview(user):
    st.markdown('<div class="section-header">Dashboard Overview</div>', unsafe_allow_html=True)
    
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
            st.markdown('<div class="section-header">Recent Job Postings</div>', unsafe_allow_html=True)
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            
            for job in my_jobs[:5]:
                st.markdown('<div class="job-item">', unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f'<div class="job-item-title">{job["title"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="job-item-meta">{job["company"]} • {job["location"]} • {job["category"]} - {job["subcategory"]}</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                        <div style='text-align: center;'>
                            <div class='stat-value'>{job.get('views', 0)}</div>
                            <div class='stat-label'>Views</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                        <div style='text-align: center;'>
                            <div class='stat-value'>{job.get('applications_count', 0)}</div>
                            <div class='stat-label'>Applications</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.info("No jobs posted yet. Click 'Post New Job' to get started!")
            st.markdown('</div>', unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Error loading overview: {str(e)}")

def show_post_job(user):
    st.markdown('<div class="section-header">Post a New Job</div>', unsafe_allow_html=True)
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.caption("Fill in the details to create a job listing")
    st.markdown("<br>", unsafe_allow_html=True)
    
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
        
        submitted = st.form_submit_button("Post Job", type="primary", use_container_width=True)
        
        if submitted:
            if not all([title, company, location, category, subcategory, description, skills_input]):
                st.error("Please fill all required fields")
            elif not title.strip() or not company.strip() or not description.strip():
                st.error("Title, Company, and Description cannot be empty")
            elif salary_min >= salary_max:
                st.error("Maximum salary must be greater than minimum salary")
            elif salary_min < 0 or salary_max < 0:
                st.error("Salaries cannot be negative")
            else:
                try:
                    skills_required = [s.strip() for s in skills_input.split(',') if s.strip()]
                    
                    if not skills_required:
                        st.error("Please enter at least one skill")
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
                            st.success("Job posted successfully!")
                            st.balloons()
                            st.session_state['recruiter_view'] = 'manage'
                            st.rerun()
                        else:
                            st.error("Failed to post job")
                            
                except Exception as e:
                    st.error(f"Error posting job: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_manage_jobs(user):
    st.markdown('<div class="section-header">Manage Jobs & Applications</div>', unsafe_allow_html=True)
    
    try:
        jobs_collection = get_collection("jobs")
        my_jobs = Job.find_by_recruiter(jobs_collection, str(user['_id']))
        
        if not my_jobs:
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.info("No jobs posted yet. Go to 'Post New Job' to create your first job posting!")
            st.markdown('</div>', unsafe_allow_html=True)
            return
        
        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            filter_status = st.selectbox("Filter by Status", ["All", "Active", "Closed"])
        
        filtered_jobs = my_jobs
        if filter_status == "Active":
            filtered_jobs = [j for j in my_jobs if j['status'] == 'active']
        elif filter_status == "Closed":
            filtered_jobs = [j for j in my_jobs if j['status'] != 'active']
        
        st.write(f"**{len(filtered_jobs)} jobs found**")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        for job in filtered_jobs:
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            
            # Job header
            col_title, col_status = st.columns([4, 1])
            
            with col_title:
                st.markdown(f'<div class="job-item-title">{job["title"]} at {job["company"]}</div>', unsafe_allow_html=True)
            
            with col_status:
                if job['status'] == 'active':
                    st.markdown('<span class="status-badge status-active">Active</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="status-badge status-closed">Closed</span>', unsafe_allow_html=True)
            
            st.markdown("<hr style='margin: 1rem 0; border: 0; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)
            
            # Job details
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.write(f"**Location:** {job['location']}")
                st.write(f"**Category:** {job['category']}")
                st.write(f"**Role:** {job['subcategory']}")
                st.write(f"**Salary:** ${job.get('salary_min', 0):,} - ${job.get('salary_max', 0):,}")
            
            with col2:
                st.write(f"**Employment:** {job.get('employment_type', 'N/A')}")
                st.write(f"**Experience:** {job.get('experience_level', 'N/A')}")
                st.write(f"**Skills:** {', '.join(job.get('skills_required', [])[:3])}...")
            
            with col3:
                st.markdown(f"""
                    <div style='text-align: center;'>
                        <div class='stat-value'>{job.get('views', 0)}</div>
                        <div class='stat-label'>Views</div>
                    </div>
                """, unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown(f"""
                    <div style='text-align: center;'>
                        <div class='stat-value'>{job.get('applications_count', 0)}</div>
                        <div class='stat-label'>Applications</div>
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            with st.expander("View Full Details"):
                st.write("**Description:**")
                st.write(job['description'])
                
                if job.get('skills_required'):
                    st.write("**Required Skills:**")
                    st.write(", ".join(job['skills_required']))
                
                st.markdown("<br>", unsafe_allow_html=True)
                col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])
                
                with col_btn1:
                    if job['status'] == 'active':
                        if st.button("Close Job", key=f"close_{job['_id']}", use_container_width=True):
                            try:
                                jobs_collection.update_one(
                                    {"_id": job['_id']},
                                    {"$set": {"status": "closed"}}
                                )
                                st.success("Job closed")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error closing job: {str(e)}")
                
                with col_btn2:
                    if st.button("Delete", key=f"delete_{job['_id']}", use_container_width=True):
                        try:
                            jobs_collection.delete_one({"_id": job['_id']})
                            st.success("Job deleted")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error deleting job: {str(e)}")
            
            # Display applications
            apps_collection = get_collection("applications")
            applications = Application.find_by_job(apps_collection, str(job['_id']))
            
            if applications:
                st.markdown("<hr style='margin: 1.5rem 0; border: 0; border-top: 2px solid #e2e8f0;'>", unsafe_allow_html=True)
                st.markdown(f'<div class="section-header" style="margin-top: 1rem;">Applications ({len(applications)})</div>', unsafe_allow_html=True)
                
                for app in applications:
                    st.markdown('<div class="applicant-item">', unsafe_allow_html=True)
                    
                    col_app1, col_app2, col_app3, col_app4 = st.columns([2, 1, 1, 1])
                    
                    with col_app1:
                        st.markdown(f'<div class="applicant-name">{app["user_name"]}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="applicant-email">{app["user_email"]}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="applicant-date">Applied: {app["applied_at"].strftime("%Y-%m-%d %H:%M")}</div>', unsafe_allow_html=True)
                    
                    with col_app2:
                        status = app['status']
                        if status == 'pending':
                            st.markdown('<span class="status-badge status-pending">Pending</span>', unsafe_allow_html=True)
                        elif status == 'accepted':
                            st.markdown('<span class="status-badge status-accepted">Accepted</span>', unsafe_allow_html=True)
                        else:
                            st.markdown('<span class="status-badge status-rejected">Rejected</span>', unsafe_allow_html=True)
                    
                    with col_app3:
                        if app.get('resume_filename'):
                            try:
                                if resume_exists(app['resume_filename']):
                                    resume_data = get_resume_data(app['resume_filename'])
                                    
                                    if resume_data:
                                        file_extension = app['resume_filename'].split('.')[-1]
                                        st.download_button(
                                            label="Download Resume",
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
        st.error(f"Error loading jobs: {str(e)}")