import streamlit as st
from coding import main

if "base_url" not in st.session_state:
    st.session_state["base_url"] = ""
if "login_url" not in st.session_state:
    st.session_state["login_url"] = ""
if "username" not in st.session_state:
            st.session_state["username"] = ""
if "password" not in st.session_state:
    st.session_state["password"] = ""

st.subheader("Welcome to text to QA testing 🛫")
st.write("Enter Website Credential Details")

# Form for entering API details
if st.session_state["base_url"] == "":
    with st.form(key="api_details_form"):
        base_url = st.text_input("Base URL", "")
        login_url = st.text_input("Login URL", "")
        username = st.text_input("Username", "user")
        password = st.text_input("Password", type="password")

        submit_button = st.form_submit_button(label="Submit")

        # Save form data to session state
        if submit_button:
            st.session_state["base_url"] = base_url
            st.session_state["login_url"] = login_url
            st.session_state["username"] = username
            st.session_state["password"] = password
            st.success("API details have been saved to session state.")

# Display session state details
if st.session_state["base_url"] != "":
    st.write("Session State Details:")
    st.write(f"Base URL: {st.session_state['base_url']}")
    st.write(f"Login URL: {st.session_state['login_url']}")
    st.write(f"Username: {st.session_state['username']}")
    st.write(f"Password: {st.session_state['password']}")

    with st.form(key="query_form"):
        st.warning('This is page is given with data of all the Urls of the site of HRMS', icon="⚠️")
        query = st.text_input("query", "")

        submit_button_3 = st.form_submit_button(label="Submit")
        if submit_button_3:
            main(query)