import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

# ---------- DATABASE CONNECTION ----------
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Adil@#996",
        database="iot_air_quality"
    )

# ---------- LOAD DATA ----------
def load_data():
    conn = connect_db()
    query = "SELECT * FROM air_quality_data ORDER BY timestamp DESC LIMIT 100"
    df = pd.read_sql(query, conn)
    conn.close()
    return df.sort_values("timestamp")

# ---------- AQI STATUS ----------
def aqi_status(aqi):
    if aqi == 1: return "Good 😊"
    if aqi == 2: return "Fair 🙂"
    if aqi == 3: return "Moderate 😐"
    if aqi == 4: return "Poor 😷"
    if aqi == 5: return "Very Poor ☠️"
    return "Unknown"

# ---------- STREAMLIT UI ----------
st.title("🌍 Smart City Air Quality Dashboard")

df = load_data()

latest = df.iloc[-1]

st.metric("Current AQI", latest["aqi"], aqi_status(latest["aqi"]))

st.subheader("AQI Trend")
plt.figure()
plt.plot(df["timestamp"], df["aqi"])
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(plt)

st.subheader("Pollution Components")
st.write(latest[["pm2_5","pm10","co","no2","o3"]])