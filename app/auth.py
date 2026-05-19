import streamlit as st


USERS = {
    "admin": {
        "password": "admin123",
        "role": "Data Science Admin"
    },
    "executive": {
        "password": "exec123",
        "role": "Executive"
    },
    "operations": {
        "password": "ops123",
        "role": "Operations Manager"
    },
    "clinical": {
        "password": "clinical123",
        "role": "Clinical AI Lead"
    }
}


def login():

    st.markdown("## 🔐 Enterprise Login")

    username = st.text_input("Username").strip().lower()
    password = st.text_input("Password", type="password").strip()

    if st.button("Login"):

        if username in USERS and password == USERS[username]["password"]:

            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.session_state["role"] = USERS[username]["role"]

            st.success("Login successful")
            st.rerun()

        else:
            st.error("Invalid username or password")


def check_authentication():

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    return st.session_state["authenticated"]
