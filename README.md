# Smart-City-Air-Quality
End-to-end IoT data pipeline that monitors air quality, stores data, visualizes trends, and sends alerts.
# 🌍 Smart City Air Quality Monitoring IoT System

An end-to-end IoT data pipeline that monitors real-time air pollution, stores historical data, visualizes trends, and sends automated alerts when air quality becomes dangerous.

This project simulates an IoT smart city environmental monitoring system using live API data instead of physical sensors.

---

## 🚀 Project Overview

This system continuously collects air-quality data and builds a real-time monitoring dashboard.

Pipeline:

API (Virtual Sensors) → Automation → MySQL Database → Dashboard → Email Alerts

---

## 🎯 Features

• Fetches real-time air quality data every 10 minutes  
• Stores historical pollution data in MySQL  
• Live dashboard using Streamlit  
• AQI trend visualization  
• Automated email alerts for dangerous pollution levels  
• Fully automated IoT data pipeline  

---

## 🧠 IoT Architecture

| IoT Layer | Implementation |
|---|---|
| Device Layer | OpenWeather Air Quality API |
| Connectivity | Python Requests |
| Data Processing | Python Automation Scripts |
| Storage | MySQL Database |
| Analytics | Streamlit Dashboard |
| Automation | Email Alert System |

---

## 📊 Dashboard Preview

Shows:
- Current AQI level
- Pollution metrics (PM2.5, PM10, CO, NO2, O3)
- Historical AQI trend

---

## 🛠️ Tech Stack

Python  
MySQL  
Streamlit  
OpenWeather API  
SMTP (Email Alerts)  
Matplotlib  
Pandas  

---

