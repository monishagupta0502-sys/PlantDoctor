import streamlit as st

from utils.auth import (
    create_database,
    register_user,
    login_user
)
create_database()
from utils.auth import create_database

create_database()

st.set_page_config(
    page_title="Login",
    page_icon="🔐",
    layout="centered"
)

st.markdown("""
# 🌿 PlantDoctor Pro

### Login System
""")

tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])

# =========================================================
# LOGIN
# =========================================================

with tab1:

    username = st.text_input(
        "Username",
        key="login_user"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_pass"
    )

    if st.button(
        "Login",
        use_container_width=True
    ):

        user = login_user(
            username,
            password
        )

        if user:

            st.session_state.logged_in = True

            st.session_state.username = username

            st.success(
                f"Welcome {username} 🌿"
            )

        else:

            st.error(
                "Invalid username or password"
            )

# =========================================================
# REGISTER
# =========================================================

with tab2:

    new_user = st.text_input(
        "Choose Username",
        key="new_user"
    )

    new_pass = st.text_input(
        "Choose Password",
        type="password",
        key="new_pass"
    )

    if st.button(
        "Create Account",
        use_container_width=True
    ):

        success = register_user(
            new_user,
            new_pass
        )

        if success:

            st.success(
                "Account Created Successfully 🎉"
            )

        else:

            st.error(
                "Username already exists."
            )