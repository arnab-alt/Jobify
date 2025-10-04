import bcrypt
import streamlit as st
from database.connection import get_collection
from database.models import User

def hash_password(password):
    """Hash a password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    """Verify a password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def signup(email, password, name, role):
    """Sign up a new user"""
    users = get_collection("users")
    
    if User.find_by_email(users, email):
        return False, "Email already exists"
    
    user_data = User.create(email, hash_password(password), name, role)
    result = users.insert_one(user_data)
    
    if result.inserted_id:
        return True, "Account created successfully"
    return False, "Failed to create account"

def login(email, password):
    """Login user"""
    users = get_collection("users")
    user = User.find_by_email(users, email)
    
    if user and verify_password(password, user['password_hash']):
        return True, user
    return False, None

def is_logged_in():
    """Check if user is logged in"""
    return 'user' in st.session_state

def get_current_user():
    """Get current logged in user"""
    return st.session_state.get('user', None)

def refresh_current_user():
    """Refresh current user data from database"""
    if is_logged_in():
        users = get_collection("users")
        user = User.find_by_id(users, str(st.session_state['user']['_id']))
        if user:
            st.session_state['user'] = user

def logout():
    """Logout user"""
    if 'user' in st.session_state:
        del st.session_state['user']
    if 'current_page' in st.session_state:
        del st.session_state['current_page']
    if 'search_results' in st.session_state:
        del st.session_state['search_results']