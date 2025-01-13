import streamlit as st
st.set_page_config(page_title="User Authentication App", page_icon="🔒", layout="wide")

import os
from utils.auth_utils import (
    is_logged_in,
    set_session,
    remove_session,
    validate_session,
    hash_password,
    load_users,
    save_users,
    logout_from_all_devices,
    update_session_activity,
)
from utils.profile_utils import create_user_profile, view_profile
from datetime import datetime

# Set Streamlit page configuration - MUST BE FIRST STREAMLIT COMMAND

# Initialize files if not present
for file in ["users.json", "sessions.json"]:
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump({}, f)

# Home page
def home_page():
    st.title("Welcome to Your Dashboard")
    st.write(f"Logged in as: {st.session_state['username']}")
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
    st.write("### Recent Activity")
    st.info("No recent activity to display")
    st.write("### Quick Actions")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Update Status"):
            st.write("Feature coming soon!")
    with col2:
        if st.button("Send Message"):
            st.write("Feature coming soon!")

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
                st.error("Username already exists.")
                return
            users[username] = {
                "password": hash_password(password),
                "created_at": datetime.now().isoformat(),
            }
            save_users(users)
            st.success("Signup successful! Please log in.")
            st.session_state["page"] = "login"
            st.rerun()

# Login page
def login_page():
    st.title("Login to Your Account")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            if submit:
                users = load_users()
                if username in users and users[username]["password"] == hash_password(password):
                    logout_from_all_devices(username)
                    set_session(username)
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
        st.write("Don't have an account?")
        if st.button("Sign Up"):
            st.session_state["page"] = "signup"
            st.rerun()

# Main application logic
def main():
    if is_logged_in():
        update_session_activity()
        if st.session_state.get("page") == "create_profile":
            create_user_profile(st.session_state["username"])
        elif st.session_state.get("page") == "view_profile":
            view_profile()
        else:
            home_page()
    else:
        if st.session_state.get("page") == "signup":
            signup_page()
        else:
            login_page()

if __name__ == "__main__":
    main()
