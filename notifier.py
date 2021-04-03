import requests
from datetime import datetime
from config import near_position
import smtplib
import time

MY_LAT = 34.181398
MY_LONG = -118.782680
MY_EMAIL = "example@gmail.com"
MY_PASSWORD = "password"


response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()

if sunrise <= 7:
    sunrise = sunrise - 7 + 24
else:
    sunrise = sunrise - 7

sunset = sunset - 7

while True:
    if near_position(MY_LAT, MY_LONG, iss_latitude, iss_longitude):
        if int(time_now.hour) < sunrise or int(time_now.hour) > sunset:
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.startls()
                connection.login(MY_EMAIL, MY_PASSWORD)
                connection.sendmail(from_addr=MY_EMAIL,
                                    to_addrs=MY_EMAIL,
                                    msg=f"Subject:ISS Overhead!\n\nLook Up! The ISS is above you!")
    time.sleep(60000)
