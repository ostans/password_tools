import streamlit as st
from pathlib import Path
from utils.password_score import password_score

# from utils.password_score import password_score


current_dir = Path(__file__).parent.parent
image_path = current_dir / "images" / "score.png"
try:
    st.image(str(image_path))
except Exception as e:
    st.error(f"Error loading image: {e}")

st.title("Password Strength Checker")

username = st.text_input("Enter your username")
password = st.text_input("Enter your password", type="password")

if st.button("Check Password Strength"):
    if username == "" or password == "":
        st.error("Username and password cannot be empty.")
    else:
        score, total, percent, msg = password_score(username, password)
        st.markdown(msg.replace("\n", "  \n"))
        st.markdown(f"🔐 **Final Score: {score} out of 8**")
