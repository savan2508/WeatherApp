import streamlit as st

st.title("Weather forcast for the Next Days")

place = st.text_input("Place: ")
days = st.slider(
    "Forcast Days",
    min_value=1,
    max_value=5,
    help="Select the number of the days for the forcast.",
)

option = st.selectbox("Select data to view", ("Temperature", "Sky"))

st.subheader(f"{option} for the next {days} days in {place}")
