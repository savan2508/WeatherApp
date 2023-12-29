import streamlit as st
import plotly.express as px
from backend import get_date

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

# dates = ["2023-12-10", "2023-12-11", "2023-12-12", "2023-12-13", "2023-12-14"]
#
# temperature = [10, 11, 12, 13, 14]

data = get_date(place=place, forecast="forcast", days=days, kind=option)


figure = px.line(x=dates, y=temperature, labels={"x": "Date", "y": "Temperature (C)"})
st.plotly_chart(figure)
