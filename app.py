import streamlit as st

# Page config MUST be first
st.set_page_config(
    page_title="JobHub - Find Your Dream Career",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject CSS to hide sidebar elements immediately
st.markdown("""
    <style>
        [data-testid="collapsedControl"] {
            display: none !important;
        }
        section[data-testid="stSidebar"] {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

from auth.auth import signup, login, is_logged_in, get_current_user, logout
from pages.user_dashboard import show_user_dashboard
from pages.recruiter_dashboard import show_recruiter_dashboard
from pages.profile import show_profile

# Modern, clean CSS styling
st.markdown("""
    <style>
        /* Hide Streamlit elements */
        #MainMenu, footer, header {visibility: hidden !important;}
        [data-testid="stSidebarNav"], [data-testid="collapsedControl"], 
        [data-testid="stSidebar"], section[data-testid="stSidebar"],
        button[kind="header"], [data-testid="baseButton-header"],
        button[title="Toggle sidebar"] {display: none !important;}
        
        /* Hide the hamburger menu and sidebar completely */
        [data-testid="collapsedControl"] {display: none !important;}
        section[data-testid="stSidebar"] > div {display: none !important;}
        .css-1dp5vir {display: none !important;}
        
        /* Hide anchor links on headings */
        .stMarkdown h1 a, .stMarkdown h2 a, .stMarkdown h3 a,
        .stMarkdown h4 a, .stMarkdown h5 a, .stMarkdown h6 a {
            display: none !important;
        }
        
        h1 > a, h2 > a, h3 > a, h4 > a, h5 > a, h6 > a {
            display: none !important;
        }
        
        .stMarkdown a[href^="#"] {
            display: none !important;
        }
        
        /* Global styles */
        .main {
            background: #f8fafc;
            padding: 0;
        }
        
        .block-container {
            padding: 2rem 3rem;
            max-width: 1400px;
        }
        
        /* Remove navigation bar styling */
        .nav-bar {
            display: none !important;
        }
        
        /* Remove any default margins/padding that might cause white bars */
        .element-container {
            margin: 0 !important;
        }
        
        /* Card styling */
        .card {
            background: white;
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
            margin-bottom: 1.5rem;
        }
        
        /* Buttons */
        .stButton > button {
            border-radius: 8px;
            font-weight: 500;
            transition: all 0.2s;
            border: none;
            padding: 0.5rem 1.25rem;
        }
        
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        /* Form inputs */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select,
        .stTextArea > div > div > textarea {
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            padding: 0.625rem 0.875rem;
            transition: border-color 0.2s;
        }
        
        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
            background: transparent;
            border-bottom: 1px solid #e2e8f0;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            border-radius: 8px 8px 0 0;
            padding: 0.75rem 1.5rem;
            font-weight: 500;
            color: #64748b;
            border: none;
        }
        
        .stTabs [aria-selected="true"] {
            background: white;
            color: #0f172a;
            border-bottom: 2px solid #3b82f6;
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #0f172a;
            font-weight: 600;
        }
        
        h1 {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        
        h2 {
            font-size: 1.5rem;
        }
        
        h3 {
            font-size: 1.25rem;
        }
        
        /* Auth container */
        .auth-wrapper {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 70vh;
            padding: 2rem 0;
        }
        
        .auth-container {
            background: white;
            border-radius: 12px;
            padding: 2.5rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.07);
            width: 100%;
            max-width: 500px;
            margin: 2rem auto 0 auto;
        }
        
        .auth-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .auth-header h1 {
            color: #0f172a;
            font-size: 1.875rem;
            margin-bottom: 0.5rem;
        }
        
        .auth-header p {
            color: #64748b;
            font-size: 0.95rem;
        }
        
        /* User badge */
        .user-badge {
            background: #f1f5f9;
            color: #0f172a;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-weight: 500;
            font-size: 0.9rem;
        }
        
        /* Radio buttons */
        .stRadio > label {
            font-weight: 500;
            color: #0f172a;
        }
        
        /* Messages */
        .stSuccess, .stError, .stWarning, .stInfo {
            border-radius: 8px;
            font-weight: 500;
        }
    </style>
""", unsafe_allow_html=True)

def main():
    try:
        if is_logged_in():
            user = get_current_user()
            
            if not user:
                st.error("Session error. Please login again.")
                logout()
                st.rerun()
                return
            
            # Navigation bar - simplified without wrapper
            col1, col2, col3 = st.columns([4, 1, 1])

            with col1:
                st.markdown("### 💼 JobHub")

            with col2:
                if st.button("Profile", use_container_width=True, key="nav_profile"):
                    st.session_state['current_page'] = 'profile'
                    st.rerun()

            with col3:
                if st.button("Logout", use_container_width=True, key="nav_logout"):
                    logout()
                    st.rerun()
            
            st.markdown("<hr style='margin: 1.5rem 0; border: none; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)
            
            # Show appropriate page
            current_page = st.session_state.get('current_page', 'dashboard')
            
            if current_page == 'profile':
                show_profile(user)
                if st.button("← Back to Dashboard", use_container_width=False):
                    st.session_state['current_page'] = 'dashboard'
                    st.rerun()
            else:
                if user.get('role') == 'user':
                    show_user_dashboard(user)
                elif user.get('role') == 'recruiter':
                    show_recruiter_dashboard(user)
                else:
                    st.error("Invalid user role. Please contact support.")
        
        else:
            # Auth page - Centered layout
            col_left, col_center, col_right = st.columns([1, 2, 1])
            
            with col_center:
                st.markdown("""
                    <div class="auth-header">
                        <h1>Welcome to JobHub</h1>
                        <p>Your gateway to career opportunities</p>
                    </div>
                """, unsafe_allow_html=True)
                
                tab1, tab2 = st.tabs(["Login", "Sign Up"])
                
                with tab1:
                    show_login()
                
                with tab2:
                    show_signup()
            
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.info("Please refresh the page or contact support if the issue persists.")

def show_login():
    st.markdown("### Welcome Back")
    st.caption("Enter your credentials to continue")
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.form("login_form"):
        email = st.text_input("Email Address", placeholder="your.email@example.com")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Login", type="primary", use_container_width=True)
        
        if submitted:
            if not email or not password:
                st.error("Please fill all fields")
            elif not email.strip() or not password.strip():
                st.error("Email and password cannot be empty")
            else:
                try:
                    success, user = login(email.strip(), password)
                    
                    if success:
                        st.session_state['user'] = user
                        st.session_state['current_page'] = 'dashboard'
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid email or password")
                except Exception as e:
                    st.error(f"Login error: {str(e)}")

def show_signup():
    st.markdown("### Create Account")
    st.caption("Join thousands of job seekers and recruiters")
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.form("signup_form"):
        name = st.text_input("Full Name", placeholder="John Doe")
        email = st.text_input("Email Address", placeholder="your.email@example.com")
        password = st.text_input("Password", type="password", placeholder="At least 6 characters")
        
        st.markdown("<br>", unsafe_allow_html=True)
        role = st.radio("I am a:", ["user", "recruiter"], horizontal=True, 
                       format_func=lambda x: "Job Seeker" if x == "user" else "Recruiter")
        
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Create Account", type="primary", use_container_width=True)
        
        if submitted:
            # Validation
            if not all([name, email, password]):
                st.error("Please fill all fields")
            elif not name.strip() or not email.strip() or not password.strip():
                st.error("Fields cannot be empty")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters")
            elif '@' not in email or '.' not in email:
                st.error("Please enter a valid email address")
            else:
                try:
                    success, message = signup(email.strip(), password, name.strip(), role)
                    
                    if success:
                        st.success(message + " Please login.")
                    else:
                        st.error(message)
                except Exception as e:
                    st.error(f"Signup error: {str(e)}")

if __name__ == "__main__":
    main()