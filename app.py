import streamlit as st
from datetime import datetime, timedelta
from streamlit_cookies_manager import EncryptedCookieManager

# ============================
# Configurable Constants
# ============================
SESSION_TIMEOUT_MINUTES = 10  # Session validity duration in minutes
SESSION_COOKIE_KEY = "session_start_time"  # Key for session start time in cookies
USER_CREDENTIALS = {
    "admin": "password123",  # Default admin account
    "user1": "mypassword",   # Example user account
}  # Replace with secure storage for production

# ============================
# Initialize Cookies Manager
# ============================
cookies = EncryptedCookieManager(
    prefix="secure_session_",  # Prefix for cookie keys
    password="your_secure_password"  # Encryption password (replace for production)
)

# Ensure cookies are ready
if not cookies.ready():
    st.stop()

# ============================
# Helper Functions
# ============================
def is_session_valid():
    """Check if the session is still valid."""
    session_start_time = cookies.get(SESSION_COOKIE_KEY)
    if session_start_time:
        session_start_time = datetime.strptime(session_start_time, "%Y-%m-%d %H:%M:%S")
        if datetime.now() - session_start_time < timedelta(minutes=SESSION_TIMEOUT_MINUTES):
            return True
    return False

def refresh_session():
    """Refresh the session by setting a new start time."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if cookies.get(SESSION_COOKIE_KEY) != current_time:
        cookies[SESSION_COOKIE_KEY] = current_time
        cookies.save()

def clear_session():
    """Clear the session by setting the cookie value to an empty string."""
    if cookies.get(SESSION_COOKIE_KEY):
        cookies[SESSION_COOKIE_KEY] = ""
        cookies.save()

# ============================
# UI Functions
# ============================
def login_ui():
    """Render the login interface."""
    st.title("Login to Your Account")
    st.markdown("Please log in to access the application.")
    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", type="password", placeholder="Enter your password")
    
    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            refresh_session()
            st.success("Login successful! Refreshing page...")
            st.rerun()
        else:
            st.error("Invalid credentials. Please try again.")

def main_app_ui():
    """Render the main application interface."""
    st.title("Welcome to the Secure Streamlit App")
    st.markdown("This is a session-protected application.")
    st.write("You are currently logged in.")
    
    if st.button("Logout"):
        clear_session()
        st.rerun()
def display_sidebar():
    """Display the sidebar with test credentials."""
    st.sidebar.title("Test Credentials")
    st.sidebar.markdown("Use the following credentials to test the application:")
    for username, password in USER_CREDENTIALS.items():
        st.sidebar.write(f"**Username:** {username}")
        st.sidebar.write(f"**Password:** {password}")
        st.sidebar.markdown("---")
    
    # Add the link at the bottom
    st.sidebar.markdown("### Explore More")
    st.sidebar.markdown("[Visit organization](https://nas.io/curious-pm)")


# ============================
# Main Application Logic
# ============================
display_sidebar()

if not is_session_valid():
    clear_session()
    login_ui()
else:
    main_app_ui()
