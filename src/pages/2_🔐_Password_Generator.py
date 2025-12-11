import streamlit as st
from pathlib import Path
from utils.password_generators import (
    PinGenerator,
    RandomPasswordGenerator,
    MemorablePasswordGenerator,
)


st.set_page_config(layout="centered", initial_sidebar_state="collapsed")

current_dir = Path(__file__).parent.parent
image_path = current_dir / "images" / "generator.png"
try:
    st.image(str(image_path))
except Exception as e:
    st.error(f"Error loading image: {e}")

icon_path = current_dir / "images" / "password-manager.png"
try:
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image(str(icon_path), width=75)
    with col2:
        st.title("Password Generator")
except Exception as e:
    st.error(f"Error loading sidebar image: {e}")


option = st.radio(
    "Select a password generator", ("Random Password", "Memorable Password", "Pin Code")
)

if option == "Pin Code":
    length = st.slider("Select the length of the Pin Code", 4, 32)

    generator = PinGenerator(length)
elif option == "Random Password":
    length = st.slider("Select the length of the Pin Code", 4, 32)
    include_symbols = st.toggle("include Symbols")
    include_numbers = st.toggle("include Numbers")

    generator = RandomPasswordGenerator(length, include_numbers, include_symbols)
elif option == "Memorable Password":
    num_of_words = st.slider("Select number of words", 2, 10)
    separator = st.text_input("Separator", value="-")
    capitalize = st.toggle("Capitalization")

    generator = MemorablePasswordGenerator(num_of_words, separator, capitalize)
else:
    st.error("No valid password generator option selected.")
    st.stop()

password = generator.generate()
st.write("Your password is:")
st.header(rf"``` {password} ```")
