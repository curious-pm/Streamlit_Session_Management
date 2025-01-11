# Implementing Session Management in Streamlit with user Authentication 

## Overview

This application demonstrates a user authentication system using **Streamlit**. It features user signup, login, profile management, and session management to maintain active user states. The app uses JSON files as a basic database for storing user credentials and session data.

### Features
1. **Signup**: Users can create an account with a username and password.
2. **Login**: Users can log in with their credentials.
3. **Session Management**: User sessions are maintained for 10 minutes of inactivity.
4. **Profile Management**:
   - Create/Edit a profile with full name, bio, and age.
   - View the profile.
5. **Logout**: Users can log out, which deletes their session.
6. **User-Friendly UI**: Simplistic UI with a navigation sidebar.

---

## Concepts Used

### 1. **Session Management**
Session management ensures that users don't have to re-login during their interaction with the app. This is achieved using the following steps:
- **Session State**: Uses `st.session_state` to keep track of the active user and current page.
- **Session Expiry**: Sessions are automatically invalidated after 10 minutes of inactivity.
- **JSON-based Storage**: Session data is stored in a `sessions.json` file.

### 2. **Password Hashing**
Passwords are securely stored using **SHA-256 hashing**. This prevents storing raw passwords and adds an extra layer of security.

### 3. **JSON-Based Database**
Both user and session data are stored in JSON files:
- `users.json`: Stores user credentials and optional profile information.
- `sessions.json`: Stores active session details such as username, session expiry, and last activity.

### 4. **Form Validation**
Streamlit forms ensure user input is validated before being processed (e.g., matching passwords during signup).

---

## Code Walkthrough

### 1. **File Initialization**
The app initializes `users.json` and `sessions.json` files if they don't already exist:
```python
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({}, f)

if not os.path.exists(SESSION_FILE):
    with open(SESSION_FILE, "w") as f:
        json.dump({}, f)
```

### 2. **Password Hashing**
Passwords are hashed using the `hashlib` library:
```python
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
```

### 3. **Session Management Functions**
- **Set Session**: Creates a new session with an expiry timestamp:
  ```python
  def set_session(username):
      sessions = load_sessions()
      expiry = datetime.now() + timedelta(minutes=10)
      sessions[username] = {
          "expiry": expiry.isoformat(),
          "last_activity": datetime.now().isoformat()
      }
      save_sessions(sessions)
      st.session_state["username"] = username
      st.session_state["page"] = "home"
  ```

- **Check for Active Sessions**: Validates if the current session is active:
  ```python
  def is_logged_in():
      sessions = load_sessions()
      for username, session_data in sessions.items():
          expiry = datetime.fromisoformat(session_data["expiry"])
          if expiry > datetime.now():
              st.session_state["username"] = username
              st.session_state["page"] = "home"
              return True
          else:
              remove_session(username)
      return False
  ```

- **Remove Session**: Deletes a user's session when they log out:
  ```python
  def remove_session(username=None):
      sessions = load_sessions()
      if username is None:
          username = st.session_state.get("username")
      if username and username in sessions:
          del sessions[username]
      save_sessions(sessions)
  ```

### 4. **Profile Management**
Users can create and view their profile:
- **Create Profile**: Allows users to input full name, bio, and age:
  ```python
  def create_user_profile(username):
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
  ```

- **View Profile**: Displays the stored profile information:
  ```python
  def view_profile():
      users = load_users()
      user = st.session_state["username"]
      profile = users[user].get("profile", {})
      st.write(f"**Full Name:** {profile.get('full_name', 'Not set')}")
  ```

### 5. **Page Routing**
The app determines the current page using `st.session_state` and routes to the appropriate function:
```python
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
```

---

## How to Use the App

### Prerequisites
1. Install **Streamlit**:
   ```bash
   pip install streamlit
   ```

### Running the App
1. Save the code to a file, e.g., `app.py`.
2. Run the app:
   ```bash
   streamlit run app.py
   ```
3. Open the app in your browser using the provided URL.

### User Flow
1. **Signup**: Create a new account using a username and password.
2. **Login**: Log in with the created credentials.
3. **Profile Management**:
   - Create/Edit your profile.
   - View the profile.
4. **Navigation**: Use the sidebar for navigation.
5. **Logout**: Log out to end the session.

---

## Extending the App

### Add New Features
1. **Email Verification**: Add email fields and send verification codes.
2. **Persistent Database**: Replace JSON with a proper database like SQLite or PostgreSQL.
3. **Role-Based Access**: Implement different user roles (e.g., admin, guest).

### Enhance Security
1. **Session Encryption**: Use encrypted tokens (e.g., JWT) instead of plain JSON sessions.
2. **Password Reset**: Add a password recovery feature.

### Scalability
- Deploy the app on **Streamlit Cloud**, **Heroku**, or other platforms.
- Use a cloud-hosted database for production readiness.

---

## Conclusion

This app provides a foundational understanding of user authentication and session management in Streamlit. It can be extended to more advanced systems and integrated with larger projects. Whether you're building dashboards, web apps, or admin panels, this code demonstrates how to handle user authentication securely and efficiently.