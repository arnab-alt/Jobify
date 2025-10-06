import streamlit as st
from database.connection import get_collection
from database.models import Job, Application
from utils.job_api import search_external_jobs
from utils.search_helper import (
    generate_comprehensive_search_terms,
    create_job_key,
    add_skill_match_scores,
    sort_jobs_by_relevance
)
from config import COUNTRIES, JOB_CATEGORIES
import math
import time

JOBS_PER_PAGE = 50

# Clean, professional CSS
st.markdown("""
    <style>
        /* Enhanced Job Card Container */
        .job-card {
            background: white;
            border-radius: 16px;
            padding: 2rem;
            margin: 1.5rem 0;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
            border: 1px solid #e5e7eb;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .job-card::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            height: 100%;
            width: 4px;
            background: linear-gradient(180deg, #3b82f6 0%, #2563eb 100%);
            transform: scaleY(0);
            transition: transform 0.3s ease;
        }
        
        .job-card:hover {
            box-shadow: 0 8px 24px rgba(0,0,0,0.12);
            transform: translateY(-4px);
            border-color: #3b82f6;
        }
        
        .job-card:hover::before {
            transform: scaleY(1);
        }
        
        /* Job Header Section */
        .job-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 1.25rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid #f1f5f9;
        }
        
        .job-title-section {
            flex: 1;
        }
        
        .job-number {
            display: inline-block;
            background: #f1f5f9;
            color: #64748b;
            padding: 0.25rem 0.75rem;
            border-radius: 6px;
            font-size: 0.875rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
        }
        
        .job-title {
            color: #0f172a;
            font-size: 1.5rem;
            font-weight: 700;
            margin: 0.5rem 0;
            line-height: 1.3;
            letter-spacing: -0.02em;
        }
        
        .company-info {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-top: 0.75rem;
            flex-wrap: wrap;
        }
        
        .company-name {
            color: #3b82f6;
            font-weight: 600;
            font-size: 1.1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .company-name::before {
            content: '🏢';
            font-size: 1rem;
        }
        
        .job-location {
            color: #64748b;
            font-size: 0.95rem;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }
        
        .job-location::before {
            content: '📍';
            font-size: 0.9rem;
        }
        
        /* Badge Container */
        .badge-container {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin: 1rem 0;
        }
        
        .match-badge {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-weight: 700;
            font-size: 0.9rem;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
        }
        
        .match-badge::before {
            content: '✓';
            font-size: 1rem;
        }
        
        .external-badge {
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .external-badge::before {
            content: '🌐';
            font-size: 0.9rem;
        }
        
        /* Job Metadata Grid */
        .job-meta-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin: 1.25rem 0;
            padding: 1.25rem;
            background: #f8fafc;
            border-radius: 12px;
        }
        
        .meta-item {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            color: #475569;
            font-size: 0.9rem;
            font-weight: 500;
        }
        
        .meta-icon {
            font-size: 1.2rem;
            flex-shrink: 0;
        }
        
        .meta-label {
            color: #64748b;
            font-size: 0.8rem;
            display: block;
        }
        
        .meta-value {
            color: #0f172a;
            font-weight: 600;
        }
        
        /* Job Description */
        .job-description {
            color: #475569;
            font-size: 0.95rem;
            line-height: 1.7;
            margin: 1.25rem 0;
            padding: 1rem;
            background: #fafafa;
            border-radius: 8px;
            border-left: 3px solid #e2e8f0;
        }
        
        /* Skills Section */
        .skills-section {
            margin: 1.25rem 0;
        }
        
        .skills-header {
            color: #0f172a;
            font-size: 0.9rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .skills-container {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }
        
        .skill-badge {
            background: white;
            color: #334155;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 500;
            border: 1.5px solid #e2e8f0;
            transition: all 0.2s ease;
        }
        
        .skill-badge:hover {
            border-color: #3b82f6;
            background: #eff6ff;
            color: #2563eb;
            transform: translateY(-1px);
        }
        
        .skills-more {
            color: #64748b;
            font-size: 0.85rem;
            font-weight: 500;
            padding: 0.5rem 1rem;
            background: #f8fafc;
            border-radius: 8px;
            display: inline-flex;
            align-items: center;
        }
        
        /* Action Buttons Section */
        .job-actions {
            display: flex;
            gap: 0.75rem;
            margin-top: 1.5rem;
            padding-top: 1.5rem;
            border-top: 1px solid #f1f5f9;
        }
        
        /* Application Status Indicators */
        .status-indicator {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.75rem 1.25rem;
            border-radius: 10px;
            font-weight: 600;
            font-size: 0.9rem;
        }
        
        .status-applied {
            background: #dbeafe;
            color: #1e40af;
            border: 2px solid #3b82f6;
        }
        
        .status-accepted {
            background: #d1fae5;
            color: #065f46;
            border: 2px solid #10b981;
        }
        
        .status-rejected {
            background: #fee2e2;
            color: #991b1b;
            border: 2px solid #ef4444;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .job-card {
                padding: 1.5rem;
            }
            
            .job-title {
                font-size: 1.25rem;
            }
            
            .job-meta-grid {
                grid-template-columns: 1fr;
                gap: 0.75rem;
            }
        }
    </style>
""", unsafe_allow_html=True)


def show_user_dashboard(user):
    st.markdown(f"# Welcome, {user['name']}")
    st.caption("Find your next opportunity")
    st.markdown("<br>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Search Jobs", "My Applications"])
    
    with tab1:
        show_job_search(user)
    
    with tab2:
        show_my_applications(user)

def show_job_search(user):
    st.markdown("### Find Your Dream Job")
    st.caption("Search thousands of opportunities")
    
    if 'current_page_jobs' not in st.session_state:
        st.session_state['current_page_jobs'] = 1
    
    with st.form("search_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            job_category = st.selectbox(
                "Job Category",
                ["All Categories"] + list(JOB_CATEGORIES.keys())
            )
        
        with col2:
            country = st.selectbox(
                "Location",
                ["All Countries"] + COUNTRIES
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        search_button = st.form_submit_button("Search Jobs", type="primary", use_container_width=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if search_button:
        st.session_state['current_page_jobs'] = 1
        
        try:
            with st.spinner("Searching for jobs..."):
                all_jobs = perform_enhanced_search(job_category, country, user)
                st.session_state['search_results'] = all_jobs
                st.session_state['search_params'] = {
                    'job_category': job_category,
                    'country': country
                }
        except Exception as e:
            st.error(f"Error searching jobs: {str(e)}")
            st.session_state['search_results'] = []
    
    if 'search_results' in st.session_state:
        display_paginated_results(st.session_state['search_results'], user)

def perform_enhanced_search(job_category, country, user):
    jobs_collection = get_collection("jobs")
    all_jobs = []
    seen_keys = set()
    
    # Get internal jobs
    try:
        internal_jobs = Job.find_all_active(jobs_collection)
        filtered_internal = filter_internal_jobs(internal_jobs, job_category, country)
        
        for job in filtered_internal:
            key = create_job_key(job)
            if key not in seen_keys:
                seen_keys.add(key)
                all_jobs.append(job)
    except Exception as e:
        st.warning(f"Error fetching internal jobs: {str(e)}")
    
    # Generate search terms
    search_terms = generate_comprehensive_search_terms(job_category, user)
    location_queries = get_location_queries(country)
    
    # Execute searches
    external_jobs = []
    progress_bar = st.progress(0)
    
    total_searches = len(search_terms) * len(location_queries)
    current_search = 0
    
    try:
        for location in location_queries:
            for term in search_terms:
                current_search += 1
                progress_bar.progress(min(current_search / total_searches, 1.0))
                
                if len(external_jobs) >= 200:
                    break
                
                time.sleep(0.3)
                
                try:
                    jobs = search_external_jobs(term, location, limit=15)
                    
                    for job in jobs:
                        if job and isinstance(job, dict):
                            key = create_job_key(job)
                            if key not in seen_keys:
                                seen_keys.add(key)
                                external_jobs.append(job)
                except Exception as e:
                    continue
            
            if len(external_jobs) >= 200:
                break
    except Exception as e:
        st.warning(f"Some external sources could not be searched: {str(e)}")
    finally:
        progress_bar.empty()
    
    # Filter by location
    if country != "All Countries":
        external_jobs = filter_jobs_by_location(external_jobs, country)
    
    # Add skill matching
    if user.get('skills'):
        all_jobs = add_skill_match_scores(filtered_internal + external_jobs, user['skills'])
    else:
        all_jobs.extend(external_jobs)
    
    # Sort by relevance
    all_jobs = sort_jobs_by_relevance(all_jobs)
    st.success(f"Found {len(all_jobs)} jobs")
    
    return all_jobs

def get_location_queries(country):
    if country == "All Countries":
        return ["USA", "Remote", "United Kingdom", "India", "Canada"]
    else:
        return [country, f"{country} Remote", "Remote"]

def filter_jobs_by_location(jobs, country):
    country_lower = country.lower()
    country_aliases = {
        'usa': ['usa', 'united states', 'us', 'america'],
        'uk': ['uk', 'united kingdom', 'britain', 'england'],
        'uae': ['uae', 'dubai', 'abu dhabi'],
        'india': ['india', 'bangalore', 'mumbai', 'delhi'],
        'canada': ['canada', 'toronto', 'vancouver'],
    }
    
    search_terms = country_aliases.get(country_lower, [country_lower])
    filtered = []
    
    for job in jobs:
        if not job or not isinstance(job, dict):
            continue
        location = job.get('location', '').lower()
        if any(term in location for term in search_terms) or 'remote' in location:
            filtered.append(job)
    
    return filtered

def filter_internal_jobs(jobs, job_category, country):
    filtered = []
    
    for job in jobs:
        if not job or not isinstance(job, dict):
            continue
            
        # Category filter
        if job_category != "All Categories":
            job_cat = job.get('category', '')
            job_subcat = job.get('subcategory', '')
            
            if job_cat != job_category:
                subcategories = JOB_CATEGORIES.get(job_category, [])
                if job_subcat not in subcategories:
                    if not any(sub.lower() in job_subcat.lower() or 
                             job_subcat.lower() in sub.lower() 
                             for sub in subcategories):
                        continue
        
        # Location filter
        if country != "All Countries":
            job_location = job.get('location', '').lower()
            if country.lower() not in job_location and 'remote' not in job_location:
                continue
        
        filtered.append(job)
    
    return filtered

def display_paginated_results(results, user):
    total_jobs = len(results)
    total_pages = math.ceil(total_jobs / JOBS_PER_PAGE) if total_jobs > 0 else 1
    current_page = st.session_state.get('current_page_jobs', 1)
    
    if current_page > total_pages:
        current_page = total_pages
        st.session_state['current_page_jobs'] = current_page
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"## {total_jobs} Jobs Found")
    with col2:
        if total_pages > 1:
            st.markdown(f"<p style='text-align: right; color: #64748b;'>Page {current_page} of {total_pages}</p>", unsafe_allow_html=True)
    
    if not results:
        st.info("No jobs found. Try adjusting your search filters.")
        return
    
    start_idx = (current_page - 1) * JOBS_PER_PAGE
    end_idx = min(start_idx + JOBS_PER_PAGE, total_jobs)
    
    try:
        jobs_collection = get_collection("jobs")
        apps_collection = get_collection("applications")
        
        for idx, job in enumerate(results[start_idx:end_idx], start=start_idx + 1):
            if job and isinstance(job, dict):
                display_job_card(job, idx, user, jobs_collection, apps_collection)
    except Exception as e:
        st.error(f"Error displaying jobs: {str(e)}")
    
    # Pagination controls
    if total_pages > 1:
        st.markdown('<div class="pagination-bar">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if current_page > 1:
                if st.button("← Previous", use_container_width=True):
                    st.session_state['current_page_jobs'] = current_page - 1
                    st.rerun()
        
        with col2:
            st.markdown(f"**Showing {start_idx + 1}-{end_idx} of {total_jobs}**")
        
        with col3:
            if current_page < total_pages:
                if st.button("Next →", use_container_width=True):
                    st.session_state['current_page_jobs'] = current_page + 1
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

def display_job_card(job, idx, user, jobs_collection, apps_collection):
    """Display an enhanced job card with better visual hierarchy"""
    
    # Start card
    st.markdown('<div class="job-card">', unsafe_allow_html=True)
    
    # Job Header with Title and Company
    st.markdown(f'<div class="job-number">#{idx}</div>', unsafe_allow_html=True)
    st.markdown(f'<h2 class="job-title">{job.get("title", "Untitled Position")}</h2>', unsafe_allow_html=True)
    
    # Company and Location
    company = job.get('company', 'Unknown Company')
    location = job.get('location', 'Location not specified')
    st.markdown(f'''
        <div class="company-info">
            <span class="company-name">{company}</span>
            <span class="job-location">{location}</span>
        </div>
    ''', unsafe_allow_html=True)
    
    # Badges (Match Score & External Source)
    badges_html = '<div class="badge-container">'
    if job.get('skill_match_score', 0) > 0:
        match_score = int(job['skill_match_score'])
        badges_html += f'<span class="match-badge">{match_score}% Match</span>'
    
    if job.get('source') == 'external':
        source_name = job.get('job_source', 'External')
        badges_html += f'<span class="external-badge">{source_name}</span>'
    
    badges_html += '</div>'
    st.markdown(badges_html, unsafe_allow_html=True)
    
    # Job Metadata Grid
    meta_html = '<div class="job-meta-grid">'
    
    if job.get('category'):
        meta_html += f'''
            <div class="meta-item">
                <span class="meta-icon">📂</span>
                <div>
                    <div class="meta-label">Category</div>
                    <div class="meta-value">{job['category']}</div>
                </div>
            </div>
        '''
    
    if job.get('salary_min') and job.get('salary_max'):
        meta_html += f'''
            <div class="meta-item">
                <span class="meta-icon">💰</span>
                <div>
                    <div class="meta-label">Salary Range</div>
                    <div class="meta-value">${job['salary_min']:,} - ${job['salary_max']:,}</div>
                </div>
            </div>
        '''
    
    if job.get('employment_type'):
        meta_html += f'''
            <div class="meta-item">
                <span class="meta-icon">⏰</span>
                <div>
                    <div class="meta-label">Employment Type</div>
                    <div class="meta-value">{job['employment_type']}</div>
                </div>
            </div>
        '''
    
    if job.get('experience_level'):
        meta_html += f'''
            <div class="meta-item">
                <span class="meta-icon">📊</span>
                <div>
                    <div class="meta-label">Experience Level</div>
                    <div class="meta-value">{job['experience_level']}</div>
                </div>
            </div>
        '''
    
    meta_html += '</div>'
    st.markdown(meta_html, unsafe_allow_html=True)
    
    # Job Description
    description = job.get('description', 'No description available')
    truncated_desc = description[:250] + "..." if len(description) > 250 else description
    st.markdown(f'<div class="job-description">{truncated_desc}</div>', unsafe_allow_html=True)
    
    # Skills Section
    if job.get('skills_required'):
        st.markdown('<div class="skills-section">', unsafe_allow_html=True)
        st.markdown('<div class="skills-header">Required Skills</div>', unsafe_allow_html=True)
        st.markdown('<div class="skills-container">', unsafe_allow_html=True)
        
        skills_to_show = job['skills_required'][:8]
        for skill in skills_to_show:
            st.markdown(f'<span class="skill-badge">{skill}</span>', unsafe_allow_html=True)
        
        if len(job['skills_required']) > 8:
            remaining = len(job['skills_required']) - 8
            st.markdown(f'<span class="skills-more">+{remaining} more</span>', unsafe_allow_html=True)
        
        st.markdown('</div></div>', unsafe_allow_html=True)
    
    # Action Buttons Section
    st.markdown('<div class="job-actions">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # EXTERNAL JOB
        if job.get('source') == 'external':
            apply_link = job.get('apply_link', '#')
            if apply_link and apply_link != '#':
                st.link_button("Apply on Company Website", apply_link, use_container_width=True, type="primary")
            else:
                st.warning("Application link not available")
        
        # INTERNAL JOB
        else:
            try:
                job_id = str(job['_id'])
                Job.increment_views(jobs_collection, job_id)
                
                existing = apps_collection.find_one({
                    "job_id": job_id,
                    "user_id": str(user['_id'])
                })
                
                if existing:
                    status = existing['status']
                    if status == 'pending':
                        st.markdown('<div class="status-indicator status-applied">✓ Application Submitted</div>', unsafe_allow_html=True)
                    elif status == 'accepted':
                        st.markdown('<div class="status-indicator status-accepted">🎉 Application Accepted!</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="status-indicator status-rejected">Application Not Selected</div>', unsafe_allow_html=True)
                else:
                    resume_file = st.file_uploader(
                        "Upload Resume",
                        type=['pdf', 'doc', 'docx'],
                        key=f"resume_{idx}",
                        label_visibility="collapsed"
                    )
                    
                    if st.button("Apply Now", key=f"apply_{idx}", type="primary", use_container_width=True):
                        if not resume_file:
                            st.error("Please upload your resume")
                        else:
                            try:
                                from utils.file_handler import save_resume
                                
                                with st.spinner("Submitting application..."):
                                    success, result = save_resume(resume_file, str(user['_id']))
                                    
                                    if success:
                                        app_data = Application.create(
                                            job_id,
                                            str(user['_id']),
                                            user['name'],
                                            user['email'],
                                            result
                                        )
                                        apps_collection.insert_one(app_data)
                                        Job.increment_applications(jobs_collection, job_id)
                                        st.success("Application submitted successfully!")
                                        st.balloons()
                                        st.rerun()
                                    else:
                                        st.error(result)
                            except Exception as e:
                                st.error(f"Error: {str(e)}")
                                
            except Exception as e:
                st.error(f"Error loading job: {str(e)}")
    
    with col2:
        with st.expander("View Full Details"):
            st.write("**Full Description:**")
            st.write(job.get('description', 'No description available'))
            
            if job.get('skills_required'):
                st.write("**All Required Skills:**")
                st.write(", ".join(job['skills_required']))
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close job-actions
    st.markdown('</div>', unsafe_allow_html=True)  
       
def show_my_applications(user):
    st.markdown("## My Applications")
    st.caption("Track your job applications")
    
    try:
        apps_collection = get_collection("applications")
        my_apps = Application.find_by_user(apps_collection, str(user['_id']))
        
        if not my_apps:
            st.info("You haven't applied to any jobs yet. Start searching!")
            return
        
        # Calculate stats
        pending = len([a for a in my_apps if a['status'] == 'pending'])
        accepted = len([a for a in my_apps if a['status'] == 'accepted'])
        rejected = len([a for a in my_apps if a['status'] == 'rejected'])
        
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{len(my_apps)}</div>
                    <div class="metric-label">Total Applications</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{accepted}</div>
                    <div class="metric-label">Accepted</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{pending}</div>
                    <div class="metric-label">Pending</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Filter
        filter_status = st.selectbox("Filter by Status", ["All", "Pending", "Accepted", "Rejected"])
        
        filtered_apps = my_apps
        if filter_status != "All":
            filtered_apps = [a for a in my_apps if a['status'] == filter_status.lower()]
        
        st.write(f"**{len(filtered_apps)} applications**")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display applications
        jobs_collection = get_collection("jobs")
        
        for app in filtered_apps:
            try:
                job = Job.find_by_id(jobs_collection, app['job_id'])
                
                if job:
                    st.markdown('<div class="job-card">', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f'<div class="job-title">{job.get("title", "Untitled Position")}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="company-name">{job.get("company", "Unknown Company")} • {job.get("location", "N/A")}</div>', unsafe_allow_html=True)
                        st.caption(f"Applied: {app['applied_at'].strftime('%B %d, %Y at %I:%M %p')}")
                        
                        meta_info = []
                        if job.get('category'):
                            meta_info.append(job['category'])
                        if job.get('salary_min') and job.get('salary_max'):
                            meta_info.append(f"${job['salary_min']:,} - ${job['salary_max']:,}/year")
                        
                        if meta_info:
                            st.markdown(f'<div class="job-meta">{" • ".join(meta_info)}</div>', unsafe_allow_html=True)
                    
                    with col2:
                        status = app['status']
                        if status == 'pending':
                            st.markdown('<div class="status-badge status-pending">Pending</div>', unsafe_allow_html=True)
                        elif status == 'accepted':
                            st.markdown('<div class="status-badge status-accepted">Accepted</div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="status-badge status-rejected">Rejected</div>', unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.warning("Job post no longer available")
            except Exception as e:
                st.error(f"Error loading application: {str(e)}")
                
    except Exception as e:
        st.error(f"Error loading applications: {str(e)}")