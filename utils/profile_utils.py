import streamlit as st
from utils.auth_utils import load_users, save_users

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
                "age": age,
            }
            save_users(users)
            st.success("Profile saved successfully!")
            st.session_state["page"] = "home"
            st.rerun()

def view_profile():
    users = load_users()
    profile = users[st.session_state["username"]].get("profile", {})
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
