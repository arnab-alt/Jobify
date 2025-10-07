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
from utils.file_handler import save_resume
from config import COUNTRIES, JOB_CATEGORIES
from bson import ObjectId
import math
import time

JOBS_PER_PAGE = 30

# Improved Internshala-style CSS
st.markdown("""
<style>
/* Global Styles */
* {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
}

/* Job Card - Compact Internshala Style */
.job-card {
    background: #ffffff;
    border: 1px solid #d6d6d6;
    border-radius: 8px;
    padding: 14px 18px;
    margin: 10px 0;
    transition: all 0.2s ease;
    position: relative;
}

.job-card:hover {
    box-shadow: 0 2px 16px rgba(0, 0, 0, 0.1);
    border-color: #b0b0b0;
}

/* Job Header - Compact */
.job-header {
    margin-bottom: 8px;
}

.job-title {
    font-size: 18px;
    font-weight: 600;
    color: #333;
    margin: 0 0 2px 0;
    line-height: 1.3;
}

.job-company {
    font-size: 14px;
    color: #666;
    font-weight: 400;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 8px;
}

.job-badge {
    display: inline-block;
    padding: 2px 8px;
    background: #e8f5e9;
    color: #2e7d32;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 500;
}

.external-badge {
    display: inline-block;
    padding: 2px 8px;
    background: #e3f2fd;
    color: #1565c0;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 500;
}

/* Match Score Badge */
.match-badge {
    position: absolute;
    top: 12px;
    right: 16px;
    background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
    color: white;
    padding: 4px 10px;
    border-radius: 16px;
    font-size: 11px;
    font-weight: 600;
}

/* Job Details - Compact inline row */
.job-details {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin: 6px 0;
    padding: 6px 0;
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

/* Description - Compact */
.job-description {
    margin: 8px 0;
}

.description-label {
    font-size: 13px;
    font-weight: 700;
    color: #333;
    margin-bottom: 4px;
    display: inline-block;
}

.description-text {
    font-size: 13px;
    color: #666;
    line-height: 1.5;
    display: inline;
}

/* Skills Section - Compact */
.skills-section {
    margin: 8px 0;
}

.skills-label {
    font-size: 13px;
    font-weight: 700;
    color: #333;
    margin-bottom: 0;
    display: inline-block;
    margin-right: 8px;
}

.skills-list {
    display: inline-flex;
    flex-wrap: wrap;
    gap: 5px;
    align-items: center;
}

.skill-pill {
    display: inline-block;
    padding: 3px 10px;
    background: #e8f4fd;
    color: #0066cc;
    border: 1px solid #d0e7f9;
    border-radius: 14px;
    font-size: 11px;
    font-weight: 500;
}

/* View Details Button */
.view-details-btn {
    color: #008BDC;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    margin-top: 8px;
    display: inline-block;
}

.view-details-btn:hover {
    text-decoration: underline;
}

/* Details Container */
.details-container {
    margin-top: 10px;
    padding-top: 10px;
    border-top: 1px solid #f0f0f0;
}

/* Footer - Compact */
.job-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 6px;
    padding-top: 6px;
    border-top: 1px solid #f0f0f0;
}

.job-posted {
    font-size: 11px;
    color: #888;
    display: flex;
    align-items: center;
    gap: 3px;
}

/* Custom Button Styles */
.stButton > button {
    border-radius: 4px;
    font-weight: 500;
    font-size: 14px;
    padding: 8px 20px;
    transition: all 0.2s ease;
    border: none;
}

.stButton > button[kind="primary"] {
    background: #008BDC;
    color: white;
}

.stButton > button[kind="primary"]:hover {
    background: #0077be;
}

.stButton > button[kind="secondary"] {
    background: white;
    color: #008BDC;
    border: 1px solid #008BDC !important;
}

.stButton > button[kind="secondary"]:hover {
    background: #f0f8ff;
}

/* Link button specific */
[data-testid="stLinkButton"] > a {
    background: white !important;
    color: #008BDC !important;
    border: 1px solid #008BDC !important;
    border-radius: 4px;
    padding: 8px 20px;
    text-decoration: none;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.2s ease;
    display: inline-block;
    text-align: center;
}

[data-testid="stLinkButton"] > a:hover {
    background: #f0f8ff !important;
}

/* Search Summary */
.search-summary {
    background: #f8f9fa;
    padding: 12px 18px;
    border-radius: 6px;
    border-left: 4px solid #008BDC;
    margin: 14px 0;
    font-size: 14px;
    color: #333;
}

/* Pagination */
.pagination-container {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 20px;
    margin: 28px 0;
    padding: 14px;
}

.pagination-info {
    font-weight: 500;
    color: #333;
    font-size: 14px;
}

/* Filter Section */
.filter-section {
    background: #ffffff;
    padding: 18px;
    border-radius: 8px;
    border: 1px solid #e0e0e0;
    margin-bottom: 18px;
}

/* Responsive */
@media (max-width: 768px) {
    .job-details {
        flex-direction: column;
        gap: 8px;
    }
    
    .job-footer {
        flex-direction: column;
        gap: 10px;
        align-items: stretch;
    }
}

/* Application Stats */
.stat-card {
    background: white;
    padding: 18px;
    border-radius: 8px;
    border: 1px solid #e0e0e0;
    text-align: center;
}

.stat-number {
    font-size: 30px;
    font-weight: 700;
    color: #008BDC;
    margin-bottom: 6px;
}

.stat-label {
    font-size: 13px;
    color: #666;
    font-weight: 500;
}

/* Divider */
.divider {
    height: 1px;
    background: #e0e0e0;
    margin: 8px 0;
}

/* Application Form */
.application-form {
    background: #f8f9fa;
    padding: 16px;
    border-radius: 8px;
    border: 1px solid #e0e0e0;
    margin-top: 12px;
}
</style>
""", unsafe_allow_html=True)

def show_user_dashboard(user):
    st.title("🔍 Job Search Portal")
    st.markdown("Find your perfect opportunity from thousands of listings")
    
    tab1, tab2 = st.tabs(["🔎 Search Jobs", "📋 My Applications"])
    
    with tab1:
        show_search_tab(user)
    
    with tab2:
        show_applications_tab(user)

def show_search_tab(user):
    # Filter section
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.markdown("### Search Filters")
    
    col1, col2 = st.columns(2)
    with col1:
        job_category = st.selectbox(
            "Job Category", 
            ["All Categories"] + list(JOB_CATEGORIES.keys()),
            key="job_category_select"
        )
    
    with col2:
        country = st.selectbox(
            "Location", 
            ["All Countries"] + COUNTRIES,
            key="country_select"
        )
    
    if st.button("🔍 Search Jobs", type="primary", use_container_width=True):
        with st.spinner("🔎 Searching for jobs..."):
            try:
                results = perform_enhanced_search(job_category, country, user)
                st.session_state["search_results"] = results
                st.session_state["search_params"] = {
                    "job_category": job_category,
                    "country": country
                }
                # Clear any open application forms
                if "applying_to_job" in st.session_state:
                    del st.session_state["applying_to_job"]
            except Exception as e:
                st.error(f"❌ Error searching jobs: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display search results
    if "search_results" in st.session_state:
        display_paginated_results(st.session_state["search_results"], user)

def perform_enhanced_search(job_category, country, user):
    jobs_collection = get_collection("jobs")
    all_jobs = []
    seen_keys = set()
    
    try:
        internal_jobs = Job.find_all_active(jobs_collection)
        filtered_internal = filter_internal_jobs(internal_jobs, job_category, country)
        
        for job in filtered_internal:
            key = create_job_key(job)
            if key not in seen_keys:
                seen_keys.add(key)
                all_jobs.append(job)
    except Exception as e:
        st.warning(f"⚠️ Error fetching internal jobs: {str(e)}")
    
    search_terms = generate_comprehensive_search_terms(job_category, user)
    location_queries = get_location_queries(country)
    external_jobs = []
    
    progress_bar = st.progress(0)
    total_searches = len(search_terms) * len(location_queries)
    current_search = 0
    
    try:
        for location in location_queries:
            for term in search_terms:
                current_search += 1
                progress_bar.progress(min(current_search / total_searches, 1.0))
                
                if len(external_jobs) >= 150:
                    break
                    
                time.sleep(0.2)
                
                try:
                    jobs = search_external_jobs(term, location, limit=12)
                    for job in jobs:
                        if job and isinstance(job, dict):
                            key = create_job_key(job)
                            if key not in seen_keys:
                                seen_keys.add(key)
                                external_jobs.append(job)
                except Exception as e:
                    continue
                    
            if len(external_jobs) >= 150:
                break
                
    except Exception as e:
        st.warning(f"⚠️ Some external sources could not be searched: {str(e)}")
    finally:
        progress_bar.empty()
    
    if country != "All Countries":
        external_jobs = filter_jobs_by_location(external_jobs, country)
    
    if user.get("skills"):
        all_jobs = add_skill_match_scores(filtered_internal + external_jobs, user["skills"])
    else:
        all_jobs.extend(external_jobs)
    
    all_jobs = sort_jobs_by_relevance(all_jobs)
    
    st.success(f"✅ Found {len(all_jobs)} jobs")
    return all_jobs

def get_location_queries(country):
    if country == "All Countries":
        return ["USA", "Remote", "United Kingdom", "India", "Canada"]
    else:
        return [country, f"{country} Remote", "Remote"]

def filter_jobs_by_location(jobs, country):
    country_lower = country.lower()
    country_aliases = {
        "usa": ["usa", "united states", "us", "america"],
        "uk": ["uk", "united kingdom", "britain", "england"],
        "uae": ["uae", "dubai", "abu dhabi"],
        "india": ["india", "bangalore", "mumbai", "delhi"],
        "canada": ["canada", "toronto", "vancouver"]
    }
    
    search_terms = country_aliases.get(country_lower, [country_lower])
    filtered = []
    
    for job in jobs:
        if not job or not isinstance(job, dict):
            continue
            
        location = job.get("location", "").lower()
        if any(term in location for term in search_terms) or "remote" in location:
            filtered.append(job)
            
    return filtered

def filter_internal_jobs(jobs, job_category, country):
    filtered = []
    
    for job in jobs:
        if not job or not isinstance(job, dict):
            continue
            
        if job_category != "All Categories":
            job_cat = job.get("category", "")
            job_subcat = job.get("subcategory", "")
            
            if job_cat != job_category:
                subcategories = JOB_CATEGORIES.get(job_category, [])
                if job_subcat not in subcategories:
                    if not any(sub.lower() in job_subcat.lower() or job_subcat.lower() in sub.lower() for sub in subcategories):
                        continue
        
        if country != "All Countries":
            job_location = job.get("location", "").lower()
            if country.lower() not in job_location and "remote" not in job_location:
                continue
                
        filtered.append(job)
        
    return filtered

def display_paginated_results(results, user):
    total_jobs = len(results)
    total_pages = math.ceil(total_jobs / JOBS_PER_PAGE) if total_jobs > 0 else 1
    
    current_page = st.session_state.get("current_page_jobs", 1)
    if current_page > total_pages:
        current_page = 1
        st.session_state["current_page_jobs"] = 1
    
    start_idx = (current_page - 1) * JOBS_PER_PAGE
    end_idx = min(start_idx + JOBS_PER_PAGE, total_jobs)
    
    if "search_params" in st.session_state:
        params = st.session_state["search_params"]
        st.markdown(f"""
        <div class="search-summary">
            <strong>🎯 {total_jobs} jobs found</strong> - {params.get('job_category', 'All Categories')} in {params.get('country', 'All Locations')}
        </div>
        """, unsafe_allow_html=True)
    
    if total_jobs > 0:
        st.markdown(f"**Showing {start_idx + 1}-{end_idx} of {total_jobs} jobs**")
        
        page_jobs = results[start_idx:end_idx]
        
        for idx, job in enumerate(page_jobs, start=start_idx):
            display_job_card_compact(job, idx, user)
        
        if total_pages > 1:
            st.markdown('<div class="pagination-container">', unsafe_allow_html=True)
            
            cols = st.columns([1, 3, 1])
            with cols[0]:
                if current_page > 1:
                    if st.button("← Previous", use_container_width=True):
                        st.session_state["current_page_jobs"] = current_page - 1
                        st.rerun()
            
            with cols[1]:
                st.markdown(f'<div class="pagination-info">Page {current_page} of {total_pages}</div>', 
                          unsafe_allow_html=True)
            
            with cols[2]:
                if current_page < total_pages:
                    if st.button("Next →", use_container_width=True):
                        st.session_state["current_page_jobs"] = current_page + 1
                        st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("🔍 No jobs found. Try adjusting your search criteria.")

def display_job_card_compact(job, idx, user):
    """Display job card in compact style"""
    if not job or not isinstance(job, dict):
        return
    
    job_id = str(job.get("_id")) if job.get("_id") else str(job.get("id", f"ext_{idx}"))
    source = job.get("source", "internal")
    
    # Increment view count for internal jobs (only once per session per job)
    view_key = f"viewed_job_{job_id}"
    if source == "internal" and view_key not in st.session_state:
        try:
            jobs_collection = get_collection("jobs")
            Job.increment_views(jobs_collection, job_id)
            st.session_state[view_key] = True
        except Exception as e:
            pass  # Silently fail if view increment fails
    
    # Check if user is currently applying to this job
    is_applying = st.session_state.get("applying_to_job") == job_id
    
    st.markdown('<div class="job-card">', unsafe_allow_html=True)
    
    # Match score badge (top right)
    if job.get("skill_match_score", 0) > 0:
        st.markdown(f'<div class="match-badge">⭐ {int(job["skill_match_score"])}%</div>', 
                   unsafe_allow_html=True)
    
    # Header with title and company
    st.markdown('<div class="job-header">', unsafe_allow_html=True)
    
    title = job.get("title", "Untitled Position")
    company = job.get("company", "Company Name")
    
    st.markdown(f'<h3 class="job-title">{title}</h3>', unsafe_allow_html=True)
    
    # Show different badges based on source
    if source == "external":
        job_source = job.get("job_source", "External")
        badge_html = f' <span class="external-badge">🌐 {job_source}</span>'
    else:
        badge_html = ' <span class="job-badge">Actively hiring</span>'
    
    st.markdown(f'<div class="job-company">{company}{badge_html}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Job details row
    st.markdown('<div class="job-details">', unsafe_allow_html=True)
    
    details_items = []
    
    if job.get("location"):
        details_items.append(f'<div class="job-detail-item"><span class="detail-icon">📍</span><span>{job["location"]}</span></div>')
    
    job_type = job.get("employment_type") or job.get("type")
    if job_type:
        details_items.append(f'<div class="job-detail-item"><span class="detail-icon">⏰</span><span>{job_type}</span></div>')
    
    if job.get("experience_level"):
        details_items.append(f'<div class="job-detail-item"><span class="detail-icon">📅</span><span>{job["experience_level"]}</span></div>')
    
    if job.get("salary_min") and job.get("salary_max"):
        salary_text = f"${job['salary_min']//1000}K - ${job['salary_max']//1000}K"
        details_items.append(f'<div class="job-detail-item"><span class="detail-icon">💰</span><span>{salary_text}</span></div>')
    elif job.get("salary"):
        details_items.append(f'<div class="job-detail-item"><span class="detail-icon">💰</span><span>{job["salary"]}</span></div>')
    
    for item in details_items:
        st.markdown(item, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # View Details expander
    description = job.get("description", "")
    skills = job.get("required_skills") or job.get("skills_required")
    
    skill_list = []
    if skills:
        if isinstance(skills, str):
            skill_list = [s.strip() for s in skills.split(",") if s.strip()]
        else:
            skill_list = skills
        skill_list = [s for s in skill_list if s and s.strip() and s.upper() != "NA"]
    
    has_description = description and description.strip() and description.upper() != "NA"
    has_skills = skill_list and len(skill_list) > 0
    
    if has_description or has_skills:
        with st.expander("👁️ View Details", expanded=False):
            st.markdown('<div class="details-container">', unsafe_allow_html=True)
            
            if has_description:
                st.markdown(f'<div class="job-description"><strong style="font-size: 13px; color: #333;">Description:</strong> <span class="description-text">{description}</span></div>', unsafe_allow_html=True)
            
            if has_skills:
                skills_text = ", ".join(skill_list)
                st.markdown(f'<div class="skills-section"><strong style="font-size: 13px; color: #333;">Skills Required:</strong> <span style="font-size: 13px; color: #666;">{skills_text}</span></div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown('<div class="job-footer">', unsafe_allow_html=True)
    # Format posted date
    posted_text = "Recently"
    if job.get("posted_at"):
        posted_at = job["posted_at"]
        if hasattr(posted_at, 'strftime'):
            posted_text = posted_at.strftime('%b %d, %Y')
        elif isinstance(posted_at, str):
            posted_text = posted_at
    elif job.get("created_at"):
        created_at = job["created_at"]
        if hasattr(created_at, 'strftime'):
            posted_text = created_at.strftime('%b %d, %Y')
    
    st.markdown(f'<div class="job-posted"><span>🕒</span><span>Posted: {posted_text}</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Application form or buttons
    if is_applying:
        show_inline_application_form(job, user, job_id, idx)
    else:
        # Determine button layout based on job source
        if source == "internal":
            # Internal job: Show "Apply Now" button (and optionally a View Job link if URL exists)
            col1, col2 = st.columns(2)
            
            with col1:
                # Check if already applied
                apps_collection = get_collection("applications")
                user_id = user.get("user_id") or str(user.get("_id"))
                existing_app = Application.find_by_user_and_job(apps_collection, user_id, job_id)
                
                if existing_app:
                    st.button("✓ Already Applied", disabled=True, use_container_width=True, key=f"applied_{idx}")
                else:
                    if st.button("Apply Now", key=f"apply_{idx}", type="primary", use_container_width=True):
                        st.session_state["applying_to_job"] = job_id
                        st.rerun()
            
            with col2:
                # If internal job has a URL, show it
                if job.get("url"):
                    st.link_button("View Job", job["url"], use_container_width=True)
                else:
                    st.empty()
        
        else:
            # External job: Show "Apply on [Source]" button with the apply link
            apply_link = job.get("apply_link") or job.get("url")
            job_source = job.get("job_source", "Website")
            
            if apply_link and apply_link != "#":
                st.link_button(
                    f"🔗 Apply on {job_source}", 
                    apply_link, 
                    use_container_width=True
                )
            else:
                # Fallback if no apply link is available
                st.button(
                    "❌ No Apply Link Available", 
                    disabled=True, 
                    use_container_width=True, 
                    key=f"no_link_{idx}"
                )
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_inline_application_form(job, user, job_id, idx):
    """Show inline application form"""
    st.markdown('<div class="application-form">', unsafe_allow_html=True)
    st.markdown("### 📝 Application Form")
    st.markdown(f"**Position:** {job.get('title', 'N/A')}")
    st.markdown(f"**Company:** {job.get('company', 'N/A')}")
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Use a unique key for the file uploader based on job_id
    resume_key = f"resume_upload_{job_id}"
    
    uploaded_file = st.file_uploader(
        "📎 Upload Resume (PDF/DOC/DOCX) *", 
        type=["pdf", "doc", "docx"],
        key=resume_key,
        help="Upload your latest resume"
    )
    
    # Show confirmation if file is uploaded
    if uploaded_file is not None:
        st.success(f"✅ Resume uploaded: {uploaded_file.name}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📤 Submit Application", type="primary", use_container_width=True, key=f"submit_app_{idx}"):
            if uploaded_file:
                try:
                    user_id = user.get("user_id") or str(user.get("_id"))
                    user_name = user.get("name", "Unknown")
                    user_email = user.get("email", "Unknown")
                    
                    # Save resume to GridFS
                    with st.spinner("Uploading resume..."):
                        success, result = save_resume(uploaded_file, user_id)
                    
                    if success:
                        resume_filename = result
                        
                        # Create application
                        apps_collection = get_collection("applications")
                        
                        # Check if already applied
                        existing = Application.find_by_user_and_job(apps_collection, user_id, job_id)
                        
                        if existing:
                            st.warning("⚠️ You have already applied for this job!")
                        else:
                            # Create new application
                            app = Application.create(
                                apps_collection,
                                user_id,
                                job_id,
                                resume_filename,
                                user_name,
                                user_email
                            )
                            
                            if app:
                                st.success("🎉 Application submitted successfully!")
                                
                                # Clear the applying state
                                if "applying_to_job" in st.session_state:
                                    del st.session_state["applying_to_job"]
                                
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("❌ Failed to submit application. Please try again.")
                    else:
                        st.error(f"❌ Resume upload failed: {result}")
                        
                except Exception as e:
                    st.error(f"❌ Error submitting application: {str(e)}")
            else:
                st.warning("⚠️ Please upload your resume to continue.")
    
    with col2:
        if st.button("❌ Cancel", use_container_width=True, key=f"cancel_app_{idx}"):
            # Clear applying state
            if "applying_to_job" in st.session_state:
                del st.session_state["applying_to_job"]
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_applications_tab(user):
    st.markdown("### 📋 My Applications")
    
    try:
        apps_collection = get_collection("applications")
        user_id = user.get("user_id") or str(user.get("_id"))
        my_apps = Application.find_by_user(apps_collection, user_id)
        
        if not my_apps:
            st.info("🔭 You haven't applied to any jobs yet.")
            return
        
        # Statistics
        accepted = len([a for a in my_apps if a["status"] == "accepted"])
        pending = len([a for a in my_apps if a["status"] == "pending"])
        rejected = len([a for a in my_apps if a["status"] == "rejected"])
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f'''
            <div class="stat-card">
                <div class="stat-number">{len(my_apps)}</div>
                <div class="stat-label">Total Applications</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
            <div class="stat-card">
                <div class="stat-number">{accepted}</div>
                <div class="stat-label">Accepted</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'''
            <div class="stat-card">
                <div class="stat-number">{pending}</div>
                <div class="stat-label">Pending</div>
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown('<br><br>', unsafe_allow_html=True)
        
        # Filter
        filter_status = st.selectbox(
            "Filter by Status", 
            ["All", "Pending", "Accepted", "Rejected"]
        )
        
        filtered_apps = my_apps
        if filter_status != "All":
            filtered_apps = [a for a in my_apps if a["status"] == filter_status.lower()]
        
        st.write(f"**{len(filtered_apps)} applications**")
        st.markdown('<br>', unsafe_allow_html=True)
        
        # Display applications
        jobs_collection = get_collection("jobs")
        
        for app_idx, app in enumerate(filtered_apps):
            try:
                job_id = app.get("job_id")
                job = Job.find_by_id(jobs_collection, job_id)
                
                if job:
                    # Use same card styling as search results
                    st.markdown('<div class="job-card">', unsafe_allow_html=True)
                    
                    # Status badge in top right (instead of match score)
                    status = app["status"]
                    if status == "pending":
                        st.markdown('<div class="match-badge" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);">⏳ Pending</div>', unsafe_allow_html=True)
                    elif status == "accepted":
                        st.markdown('<div class="match-badge" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);">✅ Accepted</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="match-badge" style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);">❌ Rejected</div>', unsafe_allow_html=True)
                    
                    # Header with title and company
                    st.markdown('<div class="job-header">', unsafe_allow_html=True)
                    
                    title = job.get("title", "Untitled Position")
                    company = job.get("company", "Company Name")
                    
                    st.markdown(f'<h3 class="job-title">{title}</h3>', unsafe_allow_html=True)
                    st.markdown(f'<div class="job-company">{company} <span class="job-badge">Applied</span></div>', unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Job details row
                    st.markdown('<div class="job-details">', unsafe_allow_html=True)
                    
                    details_items = []
                    
                    if job.get("location"):
                        details_items.append(f'<div class="job-detail-item"><span class="detail-icon">📍</span><span>{job["location"]}</span></div>')
                    
                    job_type = job.get("employment_type") or job.get("type")
                    if job_type:
                        details_items.append(f'<div class="job-detail-item"><span class="detail-icon">⏰</span><span>{job_type}</span></div>')
                    
                    if job.get("experience_level"):
                        details_items.append(f'<div class="job-detail-item"><span class="detail-icon">📅</span><span>{job["experience_level"]}</span></div>')
                    
                    if job.get("salary_min") and job.get("salary_max"):
                        salary_text = f"${job['salary_min']//1000}K - ${job['salary_max']//1000}K"
                        details_items.append(f'<div class="job-detail-item"><span class="detail-icon">💰</span><span>{salary_text}</span></div>')
                    
                    # Add application date
                    applied_date = app['applied_at'].strftime('%b %d, %Y')
                    details_items.append(f'<div class="job-detail-item"><span class="detail-icon">📅</span><span>Applied: {applied_date}</span></div>')
                    
                    for item in details_items:
                        st.markdown(item, unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # View Details expander
                    description = job.get("description", "")
                    skills = job.get("required_skills") or job.get("skills_required")
                    
                    skill_list = []
                    if skills:
                        if isinstance(skills, str):
                            skill_list = [s.strip() for s in skills.split(",") if s.strip()]
                        else:
                            skill_list = skills
                        skill_list = [s for s in skill_list if s and s.strip() and s.upper() != "NA"]
                    
                    has_description = description and description.strip() and description.upper() != "NA"
                    has_skills = skill_list and len(skill_list) > 0
                    
                    if has_description or has_skills or app.get("resume_filename"):
                        with st.expander("👁️ View Details", expanded=False):
                            st.markdown('<div class="details-container">', unsafe_allow_html=True)
                            
                            if has_description:
                                st.markdown(f'<div class="job-description"><strong style="font-size: 13px; color: #333;">Description:</strong> <span class="description-text">{description}</span></div>', unsafe_allow_html=True)
                            
                            if has_skills:
                                skills_text = ", ".join(skill_list)
                                st.markdown(f'<div class="skills-section"><strong style="font-size: 13px; color: #333;">Skills Required:</strong> <span style="font-size: 13px; color: #666;">{skills_text}</span></div>', unsafe_allow_html=True)
                            
                            # Resume info
                            if app.get("resume_filename"):
                                st.markdown("<br>", unsafe_allow_html=True)
                                st.markdown(f'<div style="font-size: 13px;"><strong style="color: #333;">📎 Resume Submitted:</strong> <span style="color: #666;">{app["resume_filename"]}</span></div>', unsafe_allow_html=True)
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Footer with posted date
                    st.markdown('<div class="job-footer">', unsafe_allow_html=True)
                    posted_text = job.get("posted_at", "Recently")
                    if hasattr(job.get("created_at"), 'strftime'):
                        posted_text = job["created_at"].strftime('%b %d, %Y')
                    st.markdown(f'<div class="job-posted"><span>🕒</span><span>Posted: {posted_text}</span></div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.warning("⚠️ Job post no longer available")
                    
            except Exception as e:
                st.error(f"Error loading application: {str(e)}")
                
    except Exception as e:
        st.error(f"Error loading applications: {str(e)}")
