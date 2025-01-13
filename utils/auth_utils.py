import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
import hashlib
import json
from datetime import datetime, timedelta
import secrets

DB_FILE = "users.json"
SESSION_FILE = "sessions.json"

# Initialize cookies manager
cookies = EncryptedCookieManager(
    prefix="my_app_",  # Unique prefix to prevent conflicts
    password="your-strong-password"  # Replace with a strong password
)
if not cookies.ready():
    st.stop()  # Stop execution until the cookies manager is ready

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_users(users):
    with open(DB_FILE, "w") as f:
        json.dump(users, f)

def load_sessions():
    try:
        with open(SESSION_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_sessions(sessions):
    with open(SESSION_FILE, "w") as f:
        json.dump(sessions, f)

def generate_token():
    return secrets.token_hex(16)

def set_session(username):
    sessions = load_sessions()
    if username in sessions:
        del sessions[username]
    session_token = generate_token()
    expiry = datetime.now() + timedelta(minutes=10)
    sessions[username] = {
        "token": session_token,
        "expiry": expiry.isoformat(),
        "last_activity": datetime.now().isoformat(),
    }
    save_sessions(sessions)
    st.session_state["username"] = username
    st.session_state["session_token"] = session_token
    # Set session token in a secure cookie
    cookies["session_token"] = session_token
    cookies["username"] = username
    cookies.save()

def validate_session():
    sessions = load_sessions()
    session_token = cookies.get("session_token")
    username = cookies.get("username")
    if username and session_token and username in sessions:
        session = sessions[username]
        expiry = datetime.fromisoformat(session["expiry"])
        if session["token"] == session_token and expiry > datetime.now():
            st.session_state["username"] = username
            st.session_state["session_token"] = session_token
            return True
    return False

def is_logged_in():
    return validate_session()

def remove_session(username=None):
    sessions = load_sessions()
    username = username or st.session_state.get("username")
    if username in sessions:
        del sessions[username]
    save_sessions(sessions)
    st.session_state.clear()
    # Clear cookies
    cookies["session_token"] = ""
    cookies["username"] = ""
    cookies.save()

def logout_from_all_devices(username):
    sessions = load_sessions()
    if username in sessions:
        del sessions[username]
    save_sessions(sessions)

def update_session_activity():
    sessions = load_sessions()
    username = st.session_state["username"]
    if username in sessions:
        sessions[username]["last_activity"] = datetime.now().isoformat()
        save_sessions(sessions)
