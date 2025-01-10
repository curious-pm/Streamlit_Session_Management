import streamlit as st
import hashlib
import os
import json
from datetime import datetime, timedelta

# File paths
DB_FILE = "users.json"
SESSION_FILE = "sessions.json"

# Initialize files if not present
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({}, f)

if not os.path.exists(SESSION_FILE):
    with open(SESSION_FILE, "w") as f:
        json.dump({}, f)

# Hashing passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Load users
def load_users():
    with open(DB_FILE, "r") as f:
        return json.load(f)

# Save users
def save_users(users):
    with open(DB_FILE, "w") as f:
        json.dump(users, f)

# Load sessions
def load_sessions():
    with open(SESSION_FILE, "r") as f:
        return json.load(f)

# Save sessions
def save_sessions(sessions):
    with open(SESSION_FILE, "w") as f:
        json.dump(sessions, f)

# Check for active session
def is_logged_in():
    try:
        sessions = load_sessions()
        # First check if there's a valid session file entry
        for username, session_data in sessions.items():
            expiry = datetime.fromisoformat(session_data["expiry"])
            if expiry > datetime.now():
                # Valid session found, update session state
                st.session_state["username"] = username
                st.session_state["page"] = "home"
                return True
            else:
                # Remove expired session
                remove_session(username)
        return False
    except Exception as e:
        print(f"Session check error: {e}")
        return False

# Set session
def set_session(username):
    try:
        sessions = load_sessions()
        expiry = datetime.now() + timedelta(minutes=10)  # Set session expiry to 10 minutes
        sessions[username] = {
            "expiry": expiry.isoformat(),
            "last_activity": datetime.now().isoformat()
        }
        save_sessions(sessions)
        st.session_state["username"] = username
        st.session_state["page"] = "home"
    except Exception as e:
        print(f"Error setting session: {e}")

# Remove session
def remove_session(username=None):
    try:
        sessions = load_sessions()
        if username is None:
            username = st.session_state.get("username")
        if username and username in sessions:
            del sessions[username]
        save_sessions(sessions)
        if "username" in st.session_state:
            del st.session_state["username"]
        if "page" in st.session_state:
            st.session_state["page"] = "login"
    except Exception as e:
        print(f"Error removing session: {e}")

# Update session activity
def update_session_activity():
    if "username" in st.session_state:
        sessions = load_sessions()
        username = st.session_state["username"]
        if username in sessions:
            sessions[username]["last_activity"] = datetime.now().isoformat()
            save_sessions(sessions)

def create_user_profile(username):
    st.title("Create Your Profile")
    with st.form("profile_form"):
        full_name = st.text_input("Full Name")
        bio = st.text_area("Bio")
        age = st.number_input("Age", min_value=0, max_value=150)
        submit = st.form_submit_button("Save Profile")
        
        if submit:
            users = load_users()
            users[username]["profile"] = {
                "full_name": full_name,
                "bio": bio,
                "age": age
            }
            save_users(users)
            st.success("Profile saved successfully!")
            st.session_state["page"] = "home"
            st.rerun()

def view_profile():
    users = load_users()
    user = st.session_state["username"]
    profile = users[user].get("profile", {})
    
    st.subheader("Your Profile")
    if profile:
        st.write(f"**Full Name:** {profile.get('full_name', 'Not set')}")
        st.write(f"**Bio:** {profile.get('bio', 'Not set')}")
        st.write(f"**Age:** {profile.get('age', 'Not set')}")
    else:
        st.warning("Profile not set up yet!")
        if st.button("Create Profile"):
            st.session_state["page"] = "create_profile"
            st.rerun()

# Home page
def home_page():
    st.title("Welcome to Your Dashboard")
    st.write(f"Logged in as: {st.session_state['username']}")
    
    # Sidebar with navigation
    with st.sidebar:
        st.title("Navigation")
        if st.button("View Profile"):
            st.session_state["page"] = "view_profile"
            st.rerun()
        if st.button("Edit Profile"):
            st.session_state["page"] = "create_profile"
            st.rerun()
        if st.button("Logout"):
            remove_session()
            st.session_state["page"] = "login"
            st.rerun()
    
    # Main content
    st.write("### Recent Activity")
    st.info("No recent activity to display")
    
    # Sample widgets
    st.write("### Quick Actions")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Update Status"):
            st.write("Status update feature coming soon!")
    with col2:
        if st.button("Send Message"):
            st.write("Messaging feature coming soon!")

# Signup page
def signup_page():
    st.title("Create New Account")
    with st.form("signup_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("Sign Up")
        
        if submit:
            if not username or not password:
                st.error("Username and password cannot be empty.")
                return

            if password != confirm_password:
                st.error("Passwords do not match.")
                return

            users = load_users()
            if username in users:
                st.error("Username already exists. Please choose another.")
                return

            users[username] = {
                "password": hash_password(password),
                "created_at": datetime.now().isoformat()
            }
            save_users(users)
            st.success("Signup successful! Please log in.")
            st.session_state["page"] = "login"
            st.rerun()

# Login page
def login_page():
    st.title("Login to Your Account")
    
    # Center the form on the page
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                users = load_users()
                if username in users and users[username]["password"] == hash_password(password):
                    set_session(username)
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
        
        # Add signup link
        st.write("Don't have an account?")
        if st.button("Sign Up"):
            st.session_state["page"] = "signup"
            st.rerun()

# Main application logic
def main():
    # Set page config
    st.set_page_config(
        page_title="User Authentication App",
        page_icon="🔒",
        layout="wide"
    )

    # First check if there's an active session
    if is_logged_in():
        update_session_activity()
        # User is logged in, show appropriate page
        if st.session_state.get("page") == "create_profile":
            create_user_profile(st.session_state["username"])
        elif st.session_state.get("page") == "view_profile":
            view_profile()
        else:
            home_page()
    else:
        # No active session, show login or signup page
        if st.session_state.get("page") == "signup":
            signup_page()
        else:
            login_page()

if __name__ == "__main__":
    main()
