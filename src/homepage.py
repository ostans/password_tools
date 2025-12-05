import streamlit as st
from streamlit_option_menu import option_menu


st.set_page_config(
    page_title="Password Tool",
    page_icon=":closed_lock_with_key:",
    layout="centered",
)
# Initialize session state for buttons
if st.session_state.get("password_strength_button", False):
    manual_select = 1
elif st.session_state.get("password_generator_button", False):
    manual_select = 2
else:
    manual_select = None

# Horizontal navbar
selected = option_menu(
    menu_title=None,
    options=["Home", "Password Strength", "Password Generator"],
    icons=["house", "shield", "key"],
    orientation="horizontal",
    manual_select=manual_select,
)

if selected == "Home":
    st.title("Home")
    st.write(
        "Welcome to the Password Tool! Use the navigation menu to explore different features."
    )
    st.write(
        "This application helps you assess the strength of your passwords and generate secure passwords."
    )
    st.write(
        "Select 'Password Strength' to evaluate your passwords or 'Password Generator' to create strong passwords."
    )
    col1, col2 = st.columns([1, 3])
    with col1:
        st.button(
            "Password Strength",
            key="password_strength_button",
        )
    with col2:
        st.button(
            "Password Generator",
            key="password_generator_button",
        )

elif selected == "Password Strength":
    password_score = st.navigation([st.Page("pages/1_pass_score_page.py")])
    password_score.run()

elif selected == "Password Generator":
    password_generator = st.navigation([st.Page("pages/2_pass_gen_page.py")])
    password_generator.run()
