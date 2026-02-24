import smtplib
from email.mime.text import MIMEText

EMAIL = "adilsalah697@gmail.com"
APP_PASSWORD = "owmoxfdquzzigtni"

def send_alert(aqi):
    msg = MIMEText(f"⚠️ Air Quality Alert! Current AQI level is {aqi}. Stay safe!")
    msg["Subject"] = "Air Quality Warning"
    msg["From"] = EMAIL
    msg["To"] = EMAIL

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, APP_PASSWORD)
    server.send_message(msg)
    server.quit()