import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

DATA_URL = ('/Users/Pramod/Github/python_streamlit_webapp/Project/Motor_Vehicle_Collisions_Crashes.csv')

st.title("Motor Vehicle Collisions in New York City")
st.markdown("This application is a streamlit dashboard that can be used to analyze motor vehicle collision in NYC 🗽💥🏎️")

@st.cache(persist=True) # Cache mechanism doesn't make call back again to read from the original file
def load_data (nrows):
    data = pd.read_csv(DATA_URL, nrows = nrows, parse_dates=[['CRASH_DATE', 'CRASH_TIME']])
    data.dropna(subset=['LATITUDE','LONGITUDE'], inplace = True) # dropping these colums to
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data.rename(columns={'crash_date_crash_time': 'date/time'}, inplace=True)
    return data

data = load_data(100000)

st.header("Where are the most people injured most in NYC?")
injured_people = st.slider("Number of persons injured in a vehicle collisions", 0, 19) # 19 - Number of max persons injured at a given spot
st.map(data.query("injured_persons >= @injured_people")[["latitude","longitude"]].dropna(how="any")) # Drop the persons if any value is N/A


st.header("How many collisions occur during a given time of day?")
hour = st.slider("Hour to look at",0,23)
data = data[data['date/time'].dt.hour == hour]

st.markdown("Vehiclecollisions between %i:00 and %i:00" %(hour,(hour+1) %24))

midpoint  =  (np.average(data['latitude']), np.average(data['longitude']))

st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state= {
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50,
    },
    layers = [
        pdk.Layer(
            "HexagonLayer",
            data = data[['date/time', 'latitude', 'longitude']],
            get_position=['longitude','latitude'],
            radius = 100,
            extruded = True,
            pickable=True,
            elevation_scale=4,
            elevation_range=[0,1000],
        ),
    ]
))



if st.checkbox("Show Raw Data", False):
    st.subheader('Raw Data')
    st.write(data)
