import requests
from datetime import datetime
import smtplib
import time

# print(data_lat, data_long)
# #print(data["iss_position"]["longitude"])
# """
# if response.status_code !=200:
#     raise Exception("bad response from iss api")
# else:
#     print(response.status_code)
# """



LAT = 51.054340
LNG = 3.717424

def check_zone():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    iss_lat = float(response.json()["iss_position"]["latitude"])
    iss_lng = float(response.json()["iss_position"]["longitude"])
    if iss_lat - 5 <= LAT <= iss_lat + 5 and iss_lng - 5 <= LNG <= iss_lng + 5:
        return True

def check_time():
    parameters = {
        "lat": LAT,
        "lng": LNG,
        "formatted": 0
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params = parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    # print(sunrise)
    # print(sunset)

    time_now = datetime.now()

    if time_now.hour >= sunset or time_now.hour <= sunrise:
        return True

# import os and use it to get the Github repository secrets
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")

def mailk(frommail, pwdd, subject, tomail, bericht):

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=frommail, password=pwdd)
        connection.sendmail(
            from_addr=frommail,
            to_addrs=tomail,
            msg=f"Subject:{subject}\n\n{bericht}")
        connection.close()

tmail = "ISS boven hemel...."
onderwerp = "iss boen hemel"

while True:

    if check_zone() and check_time():
        mailk(my_email, pwd, onderwerp, tmail, bericht)
    time.sleep(60)
    print(check_zone())
    print(check_time())
