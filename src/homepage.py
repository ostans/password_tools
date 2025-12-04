import streamlit as st
from streamlit_option_menu import option_menu


st.set_page_config(
    page_title="Password Tool",
    page_icon=":closed_lock_with_key:",
    layout="centered",
)
# Horizontal navbar
selected = option_menu(
    menu_title=None, 
    options=["Home", "Password Strength", "Password Generator"],
    icons=["house", "shield", "key"],  
    orientation="horizontal",
)

if selected == "Home":
    st.title("Home")
elif selected == "Password Strength":
    password_score = st.navigation([st.Page("pages/1_pass_score_page.py")])
    password_score.run()

elif selected == "Password Generator":
    pg = st.navigation([st.Page("pages/2_pass_gen_page.py")])
    pg.run()
