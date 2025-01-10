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
    sessions = load_sessions()
    user = st.session_state.get("username")
    if user and user in sessions:
        expiry = datetime.fromisoformat(sessions[user]["expiry"])
        if expiry > datetime.now():
            return True
        else:
            # Remove expired session
            remove_session()
    return False

# Set session
def set_session(username):
    sessions = load_sessions()
    expiry = datetime.now() + timedelta(days=1)  # Set session expiry to 1 day
    sessions[username] = {"expiry": expiry.isoformat()}
    save_sessions(sessions)
    st.session_state["username"] = username

# Remove session
def remove_session():
    sessions = load_sessions()
    user = st.session_state.get("username")
    if user in sessions:
        del sessions[user]
    save_sessions(sessions)
    st.session_state.pop("username", None)

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

# Home page
def home_page():
    st.title("Welcome to Your Dashboard")
    st.write(f"Logged in as: {st.session_state['username']}")
    
    # Sidebar with navigation
    with st.sidebar:
        st.title("Navigation")
        if st.button("View Profile"):
            st.session_state["page"] = "view_profile"
        if st.button("Edit Profile"):
            st.session_state["page"] = "create_profile"
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
                    st.session_state["page"] = "home"
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
    # Initialize session state
    if "page" not in st.session_state:
        st.session_state["page"] = "login"

    # Page routing
    if st.session_state["page"] == "home" and is_logged_in():
        home_page()
    elif st.session_state["page"] == "signup":
        signup_page()
    elif st.session_state["page"] == "create_profile" and is_logged_in():
        create_user_profile(st.session_state["username"])
    elif st.session_state["page"] == "view_profile" and is_logged_in():
        view_profile()
    else:
        login_page()

if __name__ == "__main__":
    st.set_page_config(
        page_title="User Authentication App",
        page_icon="🔒",
        layout="wide"
    )
    main()