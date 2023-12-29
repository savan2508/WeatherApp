import streamlit as st
import plotly.express as px
from backend import get_date
from weathermap import locationtrack

location = locationtrack.LocationTrack()

city = location.city
state = location.state
country = location.country

st.title("Weather forcast for the Next Days")

place = st.text_input("Place: ", value=f"{city}, {state}, {country}")
days = st.slider(
    "Forcast Days",
    min_value=1,
    max_value=5,
    help="Select the number of the days for the forcast.",
)

option = st.selectbox("Select data to view", ("Temperature", "Sky"))


# Submit button
submit_button = st.button("Submit")

if submit_button:
    try:
        st.subheader(f"{option} for the next {days} days in {place}")

        # Get data from backend
        data = get_date(place=place, forecast_days=days)

        if option.lower() == "temperature":
            filtered_data = [dicty["main"]["temp"] for dicty in data]
            dates = [dicty["dt_txt"] for dicty in data]

            figure = px.line(
                x=dates,
                y=filtered_data,
                title="Temperature",
                labels={"x": "Date", "y": "Temperature (F)"},
            )
            st.plotly_chart(figure)

        elif option.lower() == "sky":
            filtered_data = [dicty["weather"][0]["main"] for dicty in data]
            images_map = {
                "Clear": "images/clear.png",
                "Snow": "images/snow.png",
                "Clouds": "images/cloud.png",
                "Rain": "images/rain.png",
            }
            images_paths = [images_map[condition] for condition in filtered_data]
            st.image(images_paths, width=115)

    except Exception as e:
        st.error(f"An error occurred: {e}")
