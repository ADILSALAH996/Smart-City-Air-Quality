def calculate_sub_index(C, breakpoints):
    for bp in breakpoints:
        Clow, Chigh, Ilow, Ihigh = bp
        if Clow <= C <= Chigh:
            return ((Ihigh-Ilow)/(Chigh-Clow))*(C-Clow)+Ilow
    return 0

# PM2.5 breakpoints (CPCB simplified)
pm25_bp = [
    (0,30,0,50),(31,60,51,100),(61,90,101,200),
    (91,120,201,300),(121,250,301,400),(251,500,401,500)
]

pm10_bp = [
    (0,50,0,50),(51,100,51,100),(101,250,101,200),
    (251,350,201,300),(351,430,301,400),(431,600,401,500)
]

def calculate_real_aqi(data):
    pm25_aqi = calculate_sub_index(data["pm2_5"], pm25_bp)
    pm10_aqi = calculate_sub_index(data["pm10"], pm10_bp)

    return round(max(pm25_aqi, pm10_aqi))