import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Adil@#996",
        database="iot_air_quality"
    )

def insert_data(data):
    conn = connect_db()
    cursor = conn.cursor()

    query = """
    INSERT INTO air_quality_data
    (timestamp, aqi, pm2_5, pm10, co, no2, o3)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        data["timestamp"],
        data["aqi"],
        data["pm2_5"],
        data["pm10"],
        data["co"],
        data["no2"],
        data["o3"]
    )

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()