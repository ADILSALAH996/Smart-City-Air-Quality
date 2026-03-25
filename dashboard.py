import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import plotly.graph_objects as go
import requests

LAT = 12.9141
LON = 74.8560
CITY = "Mangalore"

st.set_page_config(page_title="Smart Air Quality", layout="wide")

# ---------- DATABASE ----------
@st.cache_data(ttl=60)
def load_data():
    engine = create_engine(
    "mysql+mysqlconnector://root:Adil%40%23996@localhost/iot_air_quality"
    )
    query = "SELECT * FROM air_quality_data ORDER BY timestamp DESC LIMIT 200"
    df = pd.read_sql(query, engine)
    return df.sort_values("timestamp")

df = load_data()
latest = df.iloc[-1]


df["date"] = pd.to_datetime(df["timestamp"]).dt.date
daily_avg = df.groupby("date")["real_aqi"].mean().reset_index()

today = daily_avg.iloc[-1]["real_aqi"]

if len(daily_avg) > 1:
    yesterday = daily_avg.iloc[-2]["real_aqi"]
    diff = int(today - yesterday)
else:
    yesterday = today
    diff = 0

avg_aqi = int(df["real_aqi"].mean())
max_aqi = int(df["real_aqi"].max())
min_aqi = int(df["real_aqi"].min())
total_readings = len(df)

def get_weather():
    API_KEY = "bc52bb5270a3e0c7ae5d829f28e04202"
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    weather = {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "wind": data["wind"]["speed"],
        "condition": data["weather"][0]["main"]
    }

    return weather


weather = get_weather()

# ---------- AQI STATUS ----------
def get_aqi_status(aqi):
    if aqi <= 50:
        return "Good 😄", "#16a34a", "Perfect day to breathe deeply!"
    elif aqi <= 100:
        return "Satisfactory 🙂", "#eab308", "Air is okay, maybe skip heavy jogging."
    elif aqi <= 200:
        return "Moderate 😐", "#f97316", "Sensitive people should slow down today."
    elif aqi <= 300:
        return "Poor 😷", "#ef4444", "Your lungs are filing a complaint."
    elif aqi <= 400:
        return "Very Poor 🤢", "#b91c1c", "Air feels like spicy soup today."
    else:
        return "Severe ☠️", "#7f1d1d", "Congratulations, you unlocked survival mode."

status_text, color, funny_msg = get_aqi_status(latest["real_aqi"])

def aqi_color(aqi):
    if aqi <= 50: return "green"
    elif aqi <= 100: return "yellow"
    elif aqi <= 200: return "orange"
    elif aqi <= 300: return "red"
    elif aqi <= 400: return "darkred"
    else: return "purple"

def aqi_gauge(aqi):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=aqi,
        title={'text': "Air Quality Index"},
        gauge={
            'axis': {'range': [0, 500]},
            'steps': [
                {'range': [0, 50], 'color': "#16a34a"},
                {'range': [50, 100], 'color': "#eab308"},
                {'range': [100, 200], 'color': "#f97316"},
                {'range': [200, 300], 'color': "#ef4444"},
                {'range': [300, 400], 'color': "#b91c1c"},
                {'range': [400, 500], 'color': "#7f1d1d"}
            ],
        }))
    fig.update_layout(height=350)
    return fig


def aqi_map(aqi):

    # radius grows with AQI
    if aqi <= 50:
        radius = 15000
    elif aqi <= 100:
        radius = 25000
    elif aqi <= 200:
        radius = 40000
    elif aqi <= 300:
        radius = 60000
    elif aqi <= 400:
        radius = 80000
    else:
        radius = 100000

    fig = go.Figure()

    # AQI circle layer
    fig.add_trace(go.Scattermapbox(
        lat=[LAT],
        lon=[LON],
        mode="markers",
        marker=dict(size=radius/2000, color=aqi_color(aqi), opacity=0.4),
        hoverinfo="text",
        text=f"{CITY} AQI: {aqi}"
    ))

    # City marker on top
    fig.add_trace(go.Scattermapbox(
        lat=[LAT],
        lon=[LON],
        mode="markers+text",
        marker=dict(size=12, color="white"),
        text=[CITY],
        textposition="top center"
    ))

    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_zoom=9,
        mapbox_center={"lat": LAT, "lon": LON},
        height=450,
        margin={"r":0,"t":0,"l":0,"b":0}
    )

    return fig

# ---------- HEADER ----------
st.title("🌍 Smart City Air Quality Dashboard")
st.caption("Real-time IoT Monitoring System")

with st.container():
    st.markdown(
        f"""
        <div style="
            background-color:{color};
            padding:30px;
            border-radius:20px;
            text-align:center;
            color:white;
            margin-bottom:20px;">
            <h1 style="margin:0;">AQI {latest['real_aqi']}</h1>
            <h3 style="margin:5px 0;">{status_text}</h3>
            <p style="margin:0;">{funny_msg}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
with st.container():
    st.markdown("## 🌍 Live Monitoring")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.plotly_chart(aqi_gauge(latest["real_aqi"]), width="stretch")

    with col2:
        st.plotly_chart(aqi_map(latest["real_aqi"]), width="stretch")

    with col3:
        st.markdown("### 🌦 Weather Conditions")

        st.metric("Temperature", f"{weather['temperature']} °C")
        st.metric("Humidity", f"{weather['humidity']} %")
        st.metric("Wind Speed", f"{weather['wind']} m/s")

        st.write(f"Condition: {weather['condition']}")

with st.container():
    st.markdown("## 📈 Historical Insights")

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Average AQI", avg_aqi)
    col2.metric("Best AQI", min_aqi)
    col3.metric("Worst AQI", max_aqi)
    col4.metric("Total Readings", total_readings)
    col5.metric("Today AQI", int(today), f"{diff:+}")


with st.container():
    st.markdown("## 📊 Pollution Analytics")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("PM2.5", f"{latest['pm2_5']:.1f}")
    col2.metric("PM10", f"{latest['pm10']:.1f}")
    col3.metric("NO2", f"{latest['no2']:.1f}")
    col4.metric("O3", f"{latest['o3']:.1f}")

    st.markdown("---")

    colA, colB = st.columns(2)

    with colA:
        fig_aqi = px.line(df, x="timestamp", y="real_aqi", title="AQI Trend")
        fig_aqi.update_layout(height=300)
        st.plotly_chart(fig_aqi, width="stretch")

    with colB:
        fig_pm = px.line(df, x="timestamp", y=["pm2_5","pm10"], title="PM2.5 vs PM10")
        fig_pm.update_layout(height=300)
        st.plotly_chart(fig_pm, width="stretch")

    st.markdown("### 📅 Daily Average AQI")

    fig_daily = px.bar(
        daily_avg,
        x="date",
        y="real_aqi",
        title="Daily Average AQI"
    )

    fig_daily.update_layout(height=300)
    st.plotly_chart(fig_daily, width="stretch")

with st.expander("📂 View Raw Data"):
    st.dataframe(df.tail(50), width="stretch")

st.caption("Auto-refresh every 60 seconds")
