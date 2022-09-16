from datetime import datetime
import requests
import smtplib
import time

your_email = "jomelsanpedro14@gmail.com"
your_password = "ilkbbhbmgozdwwgf"

# your latitute and longitude
mylat = 15.611449
mylong = 120.968834

#to check if the ISS is near you
def is_up():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    longitude = float(data["iss_position"]["longitude"])
    latitude = float(data["iss_position"]["latitude"])
    if mylat-5 <= latitude <= mylat+5 and mylong-5 <= longitude <= mylong+5:
        return True
   

#to check if it's night time
def is_night():
    #parameters for sunrise-sunset
    parameters = {
        "lat": mylat,
        "long": mylong,
        "formatted": 0
        }
    #to get sunrise and sunset data
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters,)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now =  datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True
   

while True:
    time.sleep(60)
    if is_up() and is_night():
        connection = smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(user=your_email, password=your_password)
        connection.sendmail(
            from_addr=your_email,
            to_addrs=your_email,
            msg="Subject: Look up \n\nThe ISS is above you"
        )
