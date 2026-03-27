import streamlit as st
import requests

def show_weather():
    st.title("🌦 Weather App")

    city = st.text_input("Enter City")

    if city:
        api_key = "YOUR_API_KEY"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        res = requests.get(url).json()

        if res.get("main"):
            st.write(f"🌡 Temp: {res['main']['temp']}°C")
            st.write(f"💧 Humidity: {res['main']['humidity']}%")
        else:
            st.error("City not found")