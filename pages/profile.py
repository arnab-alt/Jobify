# import streamlit as st
# from database.connection import get_collection
# from database.models import User
# from auth.auth import refresh_current_user
# from config import COUNTRIES, ALL_JOB_PROFILES

# # Enhanced CSS for profile page
# st.markdown("""
#     <style>
#         .profile-container {
#             background: white;
#             border-radius: 20px;
#             padding: 2.5rem;
#             box-shadow: 0 8px 30px rgba(0,0,0,0.12);
#         }
        
#         .profile-header {
#             text-align: center;
#             padding: 2rem 0;
#             background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#             border-radius: 15px;
#             color: white;
#             margin-bottom: 2rem;
#         }
        
#         .profile-title {
#             font-size: 2rem;
#             font-weight: 800;
#             margin-bottom: 0.5rem;
#         }
        
#         .profile-subtitle {
#             font-size: 1.1rem;
#             opacity: 0.95;
#         }
        
#         .section-header {
#             color: #2d3748;
#             font-size: 1.3rem;
#             font-weight: 700;
#             margin: 2rem 0 1rem 0;
#             padding-bottom: 0.5rem;
#             border-bottom: 3px solid #667eea;
#         }
        
#         .info-box {
#             background: #f7fafc;
#             border-radius: 10px;
#             padding: 1.5rem;
#             margin: 1rem 0;
#             border-left: 4px solid #667eea;
#         }
        
#         .form-group {
#             margin-bottom: 1.5rem;
#         }
        
#         .success-banner {
#             background: linear-gradient(135deg, #10b981 0%, #059669 100%);
#             color: white;
#             padding: 1rem 1.5rem;
#             border-radius: 10px;
#             font-weight: 600;
#             text-align: center;
#             margin: 1rem 0;
#         }
        
#         /* Form input enhancements */
#         .stTextInput > div > div > input,
#         .stTextArea > div > div > textarea,
#         .stSelectbox > div > div > select {
#             border-radius: 10px;
#             border: 2px solid #e2e8f0;
#             padding: 0.75rem;
#             font-size: 1rem;
#         }
        
#         .stTextInput > div > div > input:focus,
#         .stTextArea > div > div > textarea:focus,
#         .stSelectbox > div > div > select:focus {
#             border-color: #667eea;
#             box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
#         }
        
#         /* Labels */
#         .stTextInput > label,
#         .stTextArea > label,
#         .stSelectbox > label {
#             font-weight: 600;
#             color: #2d3748;
#             font-size: 0.95rem;
#         }
#     </style>
# """, unsafe_allow_html=True)

# def show_profile(user):
#     """Enhanced profile page"""
#     st.markdown('<div class="profile-header">', unsafe_allow_html=True)
#     st.markdown('<div class="profile-title">ðŸ‘¤ My Profile</div>', unsafe_allow_html=True)
#     st.markdown('<div class="profile-subtitle">Manage your professional information</div>', unsafe_allow_html=True)
#     st.markdown('</div>', unsafe_allow_html=True)
    
#     if user['role'] == 'user':
#         show_user_profile(user)
#     else:
#         show_recruiter_profile(user)

# def show_user_profile(user):
#     """Enhanced job seeker profile"""
#     st.markdown('<div class="profile-container">', unsafe_allow_html=True)
#     st.markdown("### ðŸŽ¯ Job Seeker Profile")
#     st.markdown("Keep your profile updated to attract the best opportunities")
    
#     with st.form("user_profile_form"):
#         st.markdown('<div class="section-header">ðŸ“‹ Basic Information</div>', unsafe_allow_html=True)
        
#         col1, col2 = st.columns(2)
        
#         with col1:
#             name = st.text_input("Full Name*", value=user.get('name', ''), placeholder="John Doe")
#             email = st.text_input("Email*", value=user.get('email', ''), disabled=True)
#             phone = st.text_input("Phone Number", value=user.get('phone', ''), placeholder="+1 234 567 8900")
#             location = st.selectbox("Location", [""] + COUNTRIES, 
#                                    index=COUNTRIES.index(user.get('location', '')) + 1 if user.get('location', '') in COUNTRIES else 0)
        
#         with col2:
#             experience = st.selectbox("Years of Experience", 
#                                      ["", "0-1 years", "1-3 years", "3-5 years", "5-10 years", "10+ years"],
#                                      index=["", "0-1 years", "1-3 years", "3-5 years", "5-10 years", "10+ years"].index(user.get('experience', '')) if user.get('experience', '') in ["", "0-1 years", "1-3 years", "3-5 years", "5-10 years", "10+ years"] else 0)
            
#             education = st.text_input("Education", value=user.get('education', ''),
#                                      placeholder="e.g., BS in Computer Science")
        
#         st.markdown('<div class="section-header">ðŸ“ About You</div>', unsafe_allow_html=True)
        
#         bio = st.text_area("Professional Bio", value=user.get('bio', ''), height=150,
#                           placeholder="Tell us about yourself, your career goals, and what you're looking for...")
        
#         st.markdown('<div class="section-header">ðŸ”§ Skills & Expertise</div>', unsafe_allow_html=True)
        
#         skills_input = st.text_area("Skills (one per line or comma-separated)", 
#                                    value="\n".join(user.get('skills', [])) if user.get('skills', []) else "",
#                                    height=120,
#                                    placeholder="e.g., Python\nJavaScript\nReact\nMachine Learning")
        
#         st.markdown('<div class="section-header">ðŸ”— Links & Documents</div>', unsafe_allow_html=True)
        
#         col3, col4 = st.columns(2)
        
#         with col3:
#             linkedin_url = st.text_input("LinkedIn Profile", value=user.get('linkedin_url', ''),
#                                         placeholder="https://linkedin.com/in/yourprofile")
#             github_url = st.text_input("GitHub Profile", value=user.get('github_url', ''),
#                                       placeholder="https://github.com/yourusername")
        
#         with col4:
#             portfolio_url = st.text_input("Portfolio Website", value=user.get('portfolio_url', ''),
#                                          placeholder="https://yourportfolio.com")
#             resume_url = st.text_input("Resume URL", value=user.get('resume_url', ''),
#                                       placeholder="https://drive.google.com/your-resume")
        
#         st.caption("* Required fields")
#         st.markdown("<br>", unsafe_allow_html=True)
        
#         submitted = st.form_submit_button("ðŸ’¾ Save Profile", type="primary", use_container_width=True)
        
#         if submitted:
#             if not name:
#                 st.error("âš ï¸ Name is required")
#             else:
#                 if skills_input:
#                     skills = []
#                     for line in skills_input.split('\n'):
#                         skills.extend([s.strip() for s in line.split(',') if s.strip()])
#                 else:
#                     skills = []
                
#                 profile_data = {
#                     'name': name,
#                     'phone': phone,
#                     'location': location,
#                     'bio': bio,
#                     'skills': skills,
#                     'experience': experience,
#                     'education': education,
#                     'resume_url': resume_url,
#                     'linkedin_url': linkedin_url,
#                     'github_url': github_url,
#                     'portfolio_url': portfolio_url
#                 }
                
#                 users_collection = get_collection("users")
#                 result = User.update_profile(users_collection, str(user['_id']), profile_data)
                
#                 if result.modified_count > 0 or result.matched_count > 0:
#                     st.markdown('<div class="success-banner">âœ… Profile updated successfully!</div>', unsafe_allow_html=True)
#                     refresh_current_user()
#                     st.balloons()
#                 else:
#                     st.error("âŒ Failed to update profile")
    
#     st.markdown('</div>', unsafe_allow_html=True)

# def show_recruiter_profile(user):
#     """Enhanced recruiter profile"""
#     st.markdown('<div class="profile-container">', unsafe_allow_html=True)
#     st.markdown("### ðŸ¢ Recruiter Profile")
#     st.markdown("Keep your company information up to date")
    
#     with st.form("recruiter_profile_form"):
#         st.markdown('<div class="section-header">ðŸ“‹ Personal Information</div>', unsafe_allow_html=True)
        
#         col1, col2 = st.columns(2)
        
#         with col1:
#             name = st.text_input("Full Name*", value=user.get('name', ''), placeholder="Jane Smith")
#             email = st.text_input("Email*", value=user.get('email', ''), disabled=True)
#             phone = st.text_input("Phone Number", value=user.get('phone', ''), placeholder="+1 234 567 8900")
        
#         with col2:
#             company = st.text_input("Company Name*", value=user.get('company', ''), placeholder="Tech Corp Inc.")
#             company_website = st.text_input("Company Website", value=user.get('company_website', ''),
#                                           placeholder="https://yourcompany.com")
#             company_size = st.selectbox("Company Size", 
#                                        ["", "1-10", "11-50", "51-200", "201-500", "501-1000", "1000+"],
#                                        index=["", "1-10", "11-50", "51-200", "201-500", "501-1000", "1000+"].index(user.get('company_size', '')) if user.get('company_size', '') in ["", "1-10", "11-50", "51-200", "201-500", "501-1000", "1000+"] else 0)
        
#         st.markdown('<div class="section-header">ðŸ¢ Company Details</div>', unsafe_allow_html=True)
        
#         location = st.selectbox("Company Location", [""] + COUNTRIES,
#                                index=COUNTRIES.index(user.get('location', '')) + 1 if user.get('location', '') in COUNTRIES else 0)
        
#         bio = st.text_area("About Company", value=user.get('bio', ''), height=180,
#                           placeholder="Tell us about your company, culture, and what makes it a great place to work...")
        
#         st.caption("* Required fields")
#         st.markdown("<br>", unsafe_allow_html=True)
        
#         submitted = st.form_submit_button("ðŸ’¾ Save Profile", type="primary", use_container_width=True)
        
#         if submitted:
#             if not all([name, company]):
#                 st.error("âš ï¸ Name and Company are required fields")
#             else:
#                 profile_data = {
#                     'name': name,
#                     'phone': phone,
#                     'company': company,
#                     'company_website': company_website,
#                     'company_size': company_size,
#                     'location': location,
#                     'bio': bio
#                 }
                
#                 users_collection = get_collection("users")
#                 result = User.update_profile(users_collection, str(user['_id']), profile_data)
                
#                 if result.modified_count > 0 or result.matched_count > 0:
#                     st.markdown('<div class="success-banner">âœ… Profile updated successfully!</div>', unsafe_allow_html=True)
#                     refresh_current_user()
#                     st.balloons()
#                 else:
#                     st.error("âŒ Failed to update profile")
    
#     st.markdown('</div>', unsafe_allow_html=True)

import streamlit as st
from database.connection import get_collection
from database.models import User
from auth.auth import refresh_current_user
from config import COUNTRIES, ALL_JOB_PROFILES

# Enhanced CSS for profile page
st.markdown("""
    <style>
        .profile-container {
            background: white;
            border-radius: 20px;
            padding: 2.5rem;
            box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        }
        
        .profile-header {
            text-align: center;
            padding: 2rem 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            color: white;
            margin-bottom: 2rem;
        }
        
        .profile-title {
            font-size: 2rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }
        
        .profile-subtitle {
            font-size: 1.1rem;
            opacity: 0.95;
        }
        
        .section-header {
            color: #2d3748;
            font-size: 1.3rem;
            font-weight: 700;
            margin: 2rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 3px solid #667eea;
        }
        
        .info-box {
            background: #f7fafc;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            border-left: 4px solid #667eea;
        }
        
        .form-group {
            margin-bottom: 1.5rem;
        }
        
        .success-banner {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 10px;
            font-weight: 600;
            text-align: center;
            margin: 1rem 0;
        }
        
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select {
            border-radius: 10px;
            border: 2px solid #e2e8f0;
            padding: 0.75rem;
            font-size: 1rem;
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus,
        .stSelectbox > div > div > select:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .stTextInput > label,
        .stTextArea > label,
        .stSelectbox > label {
            font-weight: 600;
            color: #2d3748;
            font-size: 0.95rem;
        }
    </style>
""", unsafe_allow_html=True)

def show_profile(user):
    """Enhanced profile page"""
    #st.markdown('<div class="profile-header">', unsafe_allow_html=True)
    #st.markdown('<div class="profile-title">👤 My Profile</div>', unsafe_allow_html=True)
    #st.markdown('<div class="profile-subtitle">Manage your professional information</div>', unsafe_allow_html=True)
    #st.markdown('</div>', unsafe_allow_html=True)
    
    if user['role'] == 'user':
        show_user_profile(user)
    else:
        show_recruiter_profile(user)

def show_user_profile(user):
    """Enhanced job seeker profile"""
    st.markdown('<div class="profile-container">', unsafe_allow_html=True)
    st.markdown("### 👨‍💼 Job Seeker Profile")
    st.markdown("Keep your profile updated to attract the best opportunities")
    
    with st.form("user_profile_form"):
        st.markdown('<div class="section-header">📋 Basic Information</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name*", value=user.get('name', ''), placeholder="John Doe")
            email = st.text_input("Email*", value=user.get('email', ''), disabled=True)
            phone = st.text_input("Phone Number", value=user.get('phone', ''), placeholder="+1 234 567 8900")
            location = st.selectbox("Location", [""] + COUNTRIES, 
                                   index=COUNTRIES.index(user.get('location', '')) + 1 if user.get('location', '') in COUNTRIES else 0)
        
        with col2:
            experience = st.selectbox("Years of Experience", 
                                     ["", "0-1 years", "1-3 years", "3-5 years", "5-10 years", "10+ years"],
                                     index=["", "0-1 years", "1-3 years", "3-5 years", "5-10 years", "10+ years"].index(user.get('experience', '')) if user.get('experience', '') in ["", "0-1 years", "1-3 years", "3-5 years", "5-10 years", "10+ years"] else 0)
            
            education = st.text_input("Education", value=user.get('education', ''),
                                     placeholder="e.g., BS in Computer Science")
        
        st.markdown('<div class="section-header">📝 About You</div>', unsafe_allow_html=True)
        
        bio = st.text_area("Professional Bio", value=user.get('bio', ''), height=150,
                          placeholder="Tell us about yourself, your career goals, and what you're looking for...")
        
        st.markdown('<div class="section-header">🔧 Skills & Expertise</div>', unsafe_allow_html=True)
        
        skills_input = st.text_area("Skills (one per line or comma-separated)", 
                                   value="\n".join(user.get('skills', [])) if user.get('skills', []) else "",
                                   height=120,
                                   placeholder="e.g., Python\nJavaScript\nReact\nMachine Learning")
        
        st.markdown('<div class="section-header">🔗 Links & Documents</div>', unsafe_allow_html=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            linkedin_url = st.text_input("LinkedIn Profile", value=user.get('linkedin_url', ''),
                                        placeholder="https://linkedin.com/in/yourprofile")
            github_url = st.text_input("GitHub Profile", value=user.get('github_url', ''),
                                      placeholder="https://github.com/yourusername")
        
        with col4:
            portfolio_url = st.text_input("Portfolio Website", value=user.get('portfolio_url', ''),
                                         placeholder="https://yourportfolio.com")
            resume_url = st.text_input("Resume URL", value=user.get('resume_url', ''),
                                      placeholder="https://drive.google.com/your-resume")
        
        st.caption("* Required fields")
        st.markdown("<br>", unsafe_allow_html=True)
        
        submitted = st.form_submit_button("💾 Save Profile", type="primary", use_container_width=True)
        
        if submitted:
            if not name or not name.strip():
                st.error("⚠️ Name is required")
            else:
                try:
                    # Process skills
                    skills = []
                    if skills_input:
                        for line in skills_input.split('\n'):
                            skills.extend([s.strip() for s in line.split(',') if s.strip()])
                    
                    profile_data = {
                        'name': name.strip(),
                        'phone': phone.strip() if phone else '',
                        'location': location,
                        'bio': bio.strip() if bio else '',
                        'skills': skills,
                        'experience': experience,
                        'education': education.strip() if education else '',
                        'resume_url': resume_url.strip() if resume_url else '',
                        'linkedin_url': linkedin_url.strip() if linkedin_url else '',
                        'github_url': github_url.strip() if github_url else '',
                        'portfolio_url': portfolio_url.strip() if portfolio_url else ''
                    }
                    
                    users_collection = get_collection("users")
                    result = User.update_profile(users_collection, str(user['_id']), profile_data)
                    
                    if result.modified_count > 0 or result.matched_count > 0:
                        st.markdown('<div class="success-banner">✅ Profile updated successfully!</div>', unsafe_allow_html=True)
                        refresh_current_user()
                        st.balloons()
                    else:
                        st.error("❌ Failed to update profile")
                        
                except Exception as e:
                    st.error(f"Error updating profile: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_recruiter_profile(user):
    """Enhanced recruiter profile"""
    st.markdown('<div class="profile-container">', unsafe_allow_html=True)
    st.markdown("### 💼 Recruiter Profile")
    st.markdown("Keep your company information up to date")
    
    with st.form("recruiter_profile_form"):
        st.markdown('<div class="section-header">📋 Personal Information</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name*", value=user.get('name', ''), placeholder="Jane Smith")
            email = st.text_input("Email*", value=user.get('email', ''), disabled=True)
            phone = st.text_input("Phone Number", value=user.get('phone', ''), placeholder="+1 234 567 8900")
        
        with col2:
            company = st.text_input("Company Name*", value=user.get('company', ''), placeholder="Tech Corp Inc.")
            company_website = st.text_input("Company Website", value=user.get('company_website', ''),
                                          placeholder="https://yourcompany.com")
            company_size = st.selectbox("Company Size", 
                                       ["", "1-10", "11-50", "51-200", "201-500", "501-1000", "1000+"],
                                       index=["", "1-10", "11-50", "51-200", "201-500", "501-1000", "1000+"].index(user.get('company_size', '')) if user.get('company_size', '') in ["", "1-10", "11-50", "51-200", "201-500", "501-1000", "1000+"] else 0)
        
        st.markdown('<div class="section-header">🏢 Company Details</div>', unsafe_allow_html=True)
        
        location = st.selectbox("Company Location", [""] + COUNTRIES,
                               index=COUNTRIES.index(user.get('location', '')) + 1 if user.get('location', '') in COUNTRIES else 0)
        
        bio = st.text_area("About Company", value=user.get('bio', ''), height=180,
                          placeholder="Tell us about your company, culture, and what makes it a great place to work...")
        
        st.caption("* Required fields")
        st.markdown("<br>", unsafe_allow_html=True)
        
        submitted = st.form_submit_button("💾 Save Profile", type="primary", use_container_width=True)
        
        if submitted:
            if not name or not name.strip() or not company or not company.strip():
                st.error("⚠️ Name and Company are required fields")
            else:
                try:
                    profile_data = {
                        'name': name.strip(),
                        'phone': phone.strip() if phone else '',
                        'company': company.strip(),
                        'company_website': company_website.strip() if company_website else '',
                        'company_size': company_size,
                        'location': location,
                        'bio': bio.strip() if bio else ''
                    }
                    
                    users_collection = get_collection("users")
                    result = User.update_profile(users_collection, str(user['_id']), profile_data)
                    
                    if result.modified_count > 0 or result.matched_count > 0:
                        st.markdown('<div class="success-banner">✅ Profile updated successfully!</div>', unsafe_allow_html=True)
                        refresh_current_user()
                        st.balloons()
                    else:
                        st.error("❌ Failed to update profile")
                        
                except Exception as e:
                    st.error(f"Error updating profile: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)