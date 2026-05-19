USERS = {
    "admin": {"password": "admin123", "role": "Data Science Admin"},
    "executive": {"password": "exec123", "role": "Executive"},
    "operations": {"password": "ops123", "role": "Operations Manager"},
    "clinical": {"password": "clinical123", "role": "Clinical AI Lead"}
}

if username in USERS and password == USERS[username]["password"]:
    st.session_state["authenticated"] = True
    st.session_state["role"] = USERS[username]["role"]
    st.session_state["username"] = username
    st.success("Login successful")
    st.rerun()
else:
    st.error("Invalid username or password")
