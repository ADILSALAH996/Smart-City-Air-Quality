import requests
from datetime import datetime
from database import insert_data
import schedule
import time
from email_alert import send_alert
from aqi_calculator import calculate_real_aqi

# -------- CONFIG --------
API_KEY = "bc52bb5270a3e0c7ae5d829f28e04202"
LAT = 12.9141
LON = 74.8560

def fetch_air_quality():
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={LAT}&lon={LON}&appid={API_KEY}"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Error fetching data:", response.status_code)
        return None
    
    data = response.json()
    
    aqi = data["list"][0]["main"]["aqi"]
    components = data["list"][0]["components"]
    timestamp = datetime.now()

    return {
        "timestamp": timestamp,
        "aqi": aqi,
        "pm2_5": components["pm2_5"],
        "pm10": components["pm10"],
        "co": components["co"],
        "no2": components["no2"],
        "o3": components["o3"]
    }

def aqi_status(aqi):
    status = {
        1: "Good 😊",
        2: "Fair 🙂",
        3: "Moderate 😐",
        4: "Poor 😷",
        5: "Very Poor ☠️"
    }
    return status.get(aqi, "Unknown")

def job():
    result = fetch_air_quality()
    if result:
        # ---- calculate realistic AQI first ----
        real_aqi = calculate_real_aqi(result)
        result["real_aqi"] = real_aqi

        # ---- store data ----
        insert_data(result)
        print("Data stored at", result["timestamp"], "| Real AQI:", real_aqi)

        # ---- alert condition (use real AQI now) ----
        # Always send update email
        send_alert(real_aqi)

            # If dangerous, send one extra urgent alert
        if real_aqi >= 200:
            send_alert(real_aqi)
            print("🚨 Urgent alert sent!")
            
if __name__ == "__main__":
    schedule.every(1).minutes.do(job)

    print("Air Quality Monitoring Started...")

    while True:
        schedule.run_pending()
        time.sleep(1)
