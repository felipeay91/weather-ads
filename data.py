from influxdb import InfluxDBClient
from pandas import Series
from statsmodels.tsa.arima_model import ARIMA
import numpy



hum_list = []
temp_list = []
light_list = []

# Connecting to database
client = InfluxDBClient('192.168.1.200', 8086, 'iot7', '1234', 'piroommonitor')

#Getting humidity data
results_hum = client.query('select "humidity"::field from piroommonitor;')
for result in results_hum:
    for hum in result:
        hum_list.append(hum['humidity'])

#Getting temperature data
results_temp = client.query('select "temperature"::field from piroommonitor')
for result in results_temp:
    for temp in result:
        temp_list.append(temp['temperature'])


#Getting light data
client.switch_database('light')
results_light = client.query('select "Lux"::field from light')
for result in results_light:
    for temp in result:
        light_list.append(temp['Lux'])


print("\n")
avg_temp = sum(temp_list[-20:])/20
avg_lux = sum(light_list[-20:])/20
avg_hum = sum(hum_list[-20:])/20

# Values for LUX
#
# ~13 - ~50 twilight
# ~50 - ~100 dark day
# ~100 - ~250 moderate light: not sunny
# ~250 - 500 sunny day
# >500 really sunny day

if avg_lux < 13:
    lumm = "night"

if avg_lux >= 13 and avg_lux <=50:
    lumm = "twilight"

if avg_lux > 50 and avg_lux <=100:
    lumm = "dark day"

if avg_lux > 100 and avg_lux <=250:
    lumm = "moderate light"

if avg_lux > 250 and avg_lux <=500:
    lumm = "sunny day"

if avg_lux > 500:
    lumm = "really sunny day"

print(lumm)



# Threshold for temperature
#
# <27 confortable
# 27 - 40 disconfort
# 41 - 45 great disconfort
# 46 - 54 dangerous
# >55 risk of heart attack

# Humidity percentage
#
# For winter the recommended humidity is above 30%
# During summer it is recommended between 50% and 60%

if avg_hum <= 40:
    if avg_temp < -15:
        temp = "freezing - low humidity"

    if avg_temp >= -15 and avg_temp <=-5:
        temp = "very cold - low humidity"

    if avg_temp >= -6 and avg_temp <=5:
        temp = "cold - low humidity"

    if avg_temp >= 6 and avg_temp <=15:
        temp = "cool - low humidity"

    if avg_temp >= 16 and avg_temp <=27:
        temp = "confortable - low humidity"

    if avg_temp >= 28 and avg_temp <=40:
        temp = "disconfortable - low humidity"

    if avg_temp >= 41  and avg_temp <=45:
        temp = "great disconfort - low humidity"

    if avg_temp >= 46 and avg_temp <=54:
        temp = "dangerous - low humidity"

    if avg_temp >= 55:
        temp = "really sunny day - low humidity"




if avg_hum >= 41 and avg_hum <=60:
    if avg_temp < -15:
        temp = "freezing - good humidity"

    if avg_temp >= -15 and avg_temp <=-5:
        temp = "very cold - good humidity"

    if avg_temp >= -6 and avg_temp <=5:
        temp = "cold - good humidity"

    if avg_temp >= 6 and avg_temp <=15:
        temp = "cool - good humidity"

    if avg_temp >= 16 and avg_temp <=27:
        temp = "confortable - good humidity"

    if avg_temp >= 28 and avg_temp <=40:
        temp = "disconfortable - good humidity"

    if avg_temp >= 41  and avg_temp <=45:
        temp = "great disconfort - good humidity"

    if avg_temp >= 46 and avg_temp <=54:
        temp = "dangerous - good humidity"

    if avg_temp >= 55:
        temp = "really sunny day - good humidity"




if avg_hum >= 65:
    if avg_temp < -15:
        temp = "freezing - high humidity"

    if avg_temp >= -15 and avg_temp <=-5:
        temp = "very cold - high humidity"

    if avg_temp >= -6 and avg_temp <=5:
        temp = "cold - high humidity"

    if avg_temp >= 6 and avg_temp <=15:
        temp = "cool - high humidity"

    if avg_temp >= 16 and avg_temp <=27:
        temp = "confortable - high humidity"

    if avg_temp >= 28 and avg_temp <=40:
        temp = "disconfortable - high humidity"

    if avg_temp >= 41  and avg_temp <=45:
        temp = "great disconfort - high humidity"

    if avg_temp >= 46 and avg_temp <=54:
        temp = "dangerous - high humidity"

    if avg_temp >= 55:
        temp = "really sunny day - high humidity"



if lumm == "night" and "low" in temp:
    if "freezing" in temp or "very cold" in temp or "cold" in temp:
        print("Winter advertisements - Indoor activities")

    if "cool" in temp:
        print("Spring advertisements")

    if "confortable" in temp or "disconfortable" in temp:
        print("Summer advertisements - Outdoor activities")
    if "great" in temp or "dangerous" in temp or "really" in temp:
        print("Don't advertise - warn risks")

if lumm == "sunny day" and "confortable" in temp:
    if "freezing" in temp or "very cold" in temp or "cold" in temp:
        print("Winter advertisements")

    if "cool" in temp:
        print("Spring advertisements - Outdoor activities")

    if "confortable" in temp or "disconfortable" in temp:
        print("Summer advertisements - Outdoor activities")
    if "great" in temp or "dangerous" in temp or "really" in temp:
        print("Don't advertise - warn risks")

if lumm == "really sunny day" and "high" in temp:
    if "freezing" in temp or "very cold" in temp or "cold" in temp:
        print("Winter advertisements - Warn risks")

    if "cool" in temp:
        print("Spring advertisements")

    if "confortable" in temp or "disconfortable" in temp:
        print("Summer advertisements")
    if "great" in temp or "dangerous" in temp or "really" in temp:
        print("Don't advertise - warn risks")
