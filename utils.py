from gtts import gTTS
import io
import requests
from datetime import datetime
import streamlit as st

# Text-to-speech
def text_to_speech(text, lang="en"):
    try:
        tts = gTTS(text=text, lang=lang)
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return audio_bytes
    except Exception:
        return None

# Weather API
def get_weather_forecast(date):
    try:
        date_str = date.strftime("%Y-%m-%d")
        latitude = 40.7128
        longitude = -74.0060
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min&timezone=auto&start_date={date_str}&end_date={date_str}"
        response = requests.get(url, timeout=3)
        data = response.json()
        
        if "daily" in data:
            temp_max = data["daily"]["temperature_2m_max"][0]
            temp_min = data["daily"]["temperature_2m_min"][0]
            return f"High: {temp_max}°C, Low: {temp_min}°C"
        
        return "Weather data unavailable"
    except Exception:
        return "Weather service unavailable"

# AI analysis
def generate_ai_response(prompt):
    try:
        # Simplified AI response
        return (f"**AI Insights for your reminder**:\n\n"
                f"Based on your reminder about '{prompt.split('.')[0]}', "
                f"consider preparing in advance. Set multiple alerts if it's important.")
    except Exception:
        return "AI insights unavailable"
