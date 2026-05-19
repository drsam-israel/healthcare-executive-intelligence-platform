import streamlit as st


def login():

    st.markdown("## 🔐 Enterprise Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        USERS = {
            "admin": "admin123",
            "executive": "exec123",
            "operations": "ops123",
            "clinical": "clinical123"
        }

        if username in USERS and password == USERS[username]:

            st.session_state["authenticated"] = True
            st.success("Login successful")
            st.rerun()

        else:
            st.error("Invalid username or password")


def check_authentication():

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    return st.session_state["authenticated"]
