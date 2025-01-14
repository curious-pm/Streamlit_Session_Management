# Streamlit Session Management Template

## Introduction
This project demonstrates how to implement session management in a Streamlit application. Session management ensures that users remain logged into an application for a specified duration, even across page reloads. If the session expires, the user must re-authenticate by providing their credentials.

This guide provides a detailed explanation of the code, introduces the concept of session management, and outlines how to implement it effectively in Streamlit.

---

## What is Session Management?
Session management is the practice of securely managing user interactions with a web application across multiple requests. It ensures that:

1. Users remain logged in while interacting with the application.
2. Data persists across page reloads during the session.
3. The session expires after a predefined period or upon user logout, requiring re-authentication.

In a production-level application, session management is critical for:
- Enhancing user experience.
- Maintaining security by preventing unauthorized access.
- Tracking user activities.

---

## Steps to Implement Session Management in Streamlit

### 1. Install Required Libraries
Install Streamlit and the `streamlit-cookies-manager` library for managing encrypted cookies:

```bash
pip install streamlit streamlit-cookies-manager
```

### 2. Define Constants
Set configurable parameters for the session timeout duration, cookie keys, and user credentials. For example:

```python
SESSION_TIMEOUT_MINUTES = 10  # Session validity duration in minutes
SESSION_COOKIE_KEY = "session_start_time"  # Key for session start time in cookies
USER_CREDENTIALS = {
    "admin": "password123",  # Default admin account
    "user1": "mypassword",   # Example user account
}  # Replace with secure storage for production
```

### 3. Initialize the Cookie Manager
Use the `EncryptedCookieManager` to securely store session data in cookies. Pass a unique prefix for cookie keys and a secure password for encryption:

```python
cookies = EncryptedCookieManager(
    prefix="secure_session_",  # Prefix for cookie keys
    password="your_secure_password"  # Encryption password (replace for production)
)

# Ensure cookies are ready
if not cookies.ready():
    st.stop()
```

### 4. Implement Helper Functions
- **Session Validation**: Checks if the session is still valid based on the session start time stored in cookies.

```python
def is_session_valid():
    session_start_time = cookies.get(SESSION_COOKIE_KEY)
    if session_start_time:
        session_start_time = datetime.strptime(session_start_time, "%Y-%m-%d %H:%M:%S")
        if datetime.now() - session_start_time < timedelta(minutes=SESSION_TIMEOUT_MINUTES):
            return True
    return False
```

- **Refresh Session**: Updates the session start time to extend the session.

```python
def refresh_session():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if cookies.get(SESSION_COOKIE_KEY) != current_time:
        cookies[SESSION_COOKIE_KEY] = current_time
        cookies.save()
```

- **Clear Session**: Clears the session by setting the cookie value to an empty string.

```python
def clear_session():
    if cookies.get(SESSION_COOKIE_KEY):
        cookies[SESSION_COOKIE_KEY] = ""
        cookies.save()
```

### 5. Create the UI Functions
- **Login UI**: Displays a login form and validates user credentials.

```python
def login_ui():
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
```

- **Main App UI**: Displays the application content for logged-in users.

```python
def main_app_ui():
    st.title("Welcome to the Secure Streamlit App")
    st.markdown("This is a session-protected application.")
    st.write("You are currently logged in.")
    
    if st.button("Logout"):
        clear_session()
        st.rerun()
```

### 6. Add Main Logic
The application logic determines whether to display the login or main UI based on session validity:

```python
if not is_session_valid():
    clear_session()
    login_ui()
else:
    main_app_ui()
```

---

## Code Explanation

### Constants
- **`SESSION_TIMEOUT_MINUTES`**: Defines how long the session remains valid.
- **`SESSION_COOKIE_KEY`**: The key used to store session data in cookies.
- **`USER_CREDENTIALS`**: A dictionary of username-password pairs for authentication.

### Cookies Manager
- **`EncryptedCookieManager`**: Manages cookies with encryption for secure data storage.
- **Parameters**:
  - `prefix`: Adds a unique prefix to all cookie keys to avoid conflicts.
  - `password`: Encrypts cookie data to protect it from unauthorized access.

### Helper Functions
- **`is_session_valid`**:
  - Purpose: Checks whether the session is still valid by comparing the session start time stored in the cookies with the current time.
  - Logic: If the difference between the current time and the session start time is less than the defined timeout (10 minutes), the session is valid.
  - Key Points:
    - Fetches the session start time from cookies.
    - Uses `datetime` to calculate the time difference.

- **`refresh_session`**:
  - Purpose: Updates the session start time in the cookies to extend the session validity.
  - Logic: Sets the session start time to the current time if it differs from the previously stored value.
  - Key Points:
    - Ensures cookies are saved after updating.
    - Prevents redundant updates by checking if the value has changed.

- **`clear_session`**:
  - Purpose: Logs the user out by clearing the session data.
  - Logic: Sets the session start time cookie to an empty string and saves the change.
  - Key Points:
    - Ensures cookies are updated to reflect the cleared session.
    - Does not remove the cookie entirely but invalidates it.

- **`login_ui`**:
  - Purpose: Provides a user interface for logging in.
  - Logic:
    - Displays input fields for username and password.
    - Validates the entered credentials against the predefined dictionary (`USER_CREDENTIALS`).
    - On successful login, calls `refresh_session()` and reloads the app.
  - Key Points:
    - Uses `st.text_input` for secure password entry.
    - Displays appropriate messages for success or failure.

- **`main_app_ui`**:
  - Purpose: Displays the main content of the application for logged-in users.
  - Logic:
    - Provides a logout button to clear the session and reload the app.
    - Displays a welcome message to the user.
  - Key Points:
    - Keeps the UI simple and focused on demonstrating session management.

- **Main Logic**:
  - Purpose: Determines whether to display the login or main UI.
  - Logic:
    - If the session is not valid, clears the session and displays the login UI.
    - Otherwise, displays the main application UI.

---

## Methods for Production-Level Session Management
1. **Secure Authentication**:
   - Use secure storage for user credentials (e.g., a database).
   - Implement hashed passwords with libraries like `bcrypt` or `hashlib`.

2. **Environment Variables**:
   - Store sensitive information (e.g., encryption passwords) in environment variables.

3. **Token-Based Authentication**:
   - Use JWT or OAuth tokens for robust session management.

4. **Session Expiry**:
   - Implement idle timeout or activity-based session expiration.

5. **Secure Cookies**:
   - Enable HTTP-only and secure flags for cookies to prevent client-side access.

---

## How to Run
1. Install the required libraries:

   ```bash
   pip install streamlit streamlit-cookies-manager
   ```

2. Save the code as `app.py`.

3. Run the application:

   ```bash
   streamlit run app.py
   ```

4. Use the following credentials to log in:
   - **Username**: `admin`
   - **Password**: `password123`

---

## Conclusion
This template demonstrates how to implement secure session management in Streamlit. It uses encrypted cookies to store session data and ensures a seamless user experience while maintaining security. Students can extend this template by adding advanced features like database-backed authentication or multi-user roles.

---

Feel free to explore, modify, and share this template to understand and teach session management effectively!

