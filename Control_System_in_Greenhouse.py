import requests
import machine
import network
import time
from dotenv import load_dotenv
load_dotenv()

#SSID = "true_home2G_52A"
SSID = "Natutitato"
PASSWORD = "30113011"
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.connect(SSID, PASSWORD)
while not sta.isconnected():
    print("Connecting to WiFi...")
    time.sleep(1)
print("Connected to WiFi:", SSID)


def status_gh(status, humid, humid_adj, temp):
    if status == "FALSE":
        if temp < 40:
            print("System in greenhouse is correct")
            return 1
        else:
            print("Humidity is correct: ", humid,"Temperature is not correct: ",  "Turn on fan")
            return 2
    else:
        if humid > humid_adj and temp < 40:
            print("decrease humidity to: ", humid_adj, "Fan:Turn off", "Dehumidifier:Turn on")
            return 3
        elif humid > humid_adj and temp >= 40:
            print("decrease humidity to: ", humid_adj, "Fan:Turn on", "Dehumidifier:Turn on")
            return 4
        elif humid < humid_adj and temp < 40:
            print("increase humidity to: ", humid_adj, "Fan:Turn off", "Pump(mog):Turn on")
            return 5
        elif humid < humid_adj and temp >= 40:
            print("increase humidity to: ", humid_adj, "Fan:Turn on", "Pump(mog):Turn on")
            return 6
            
            
relay_dehumid = machine.Pin(5, machine.Pin.OUT)
relay_mog = machine.Pin(26, machine.Pin.OUT)
relay_fan = machine.Pin(25, machine.Pin.OUT)

relay_dehumid.on()
relay_mog.on()
relay_fan.on()

url = os.getenv("MONGODB_URL")
response = requests.get(url)
data = response.json()
temp = data["Temperature"]
status = data["Status"]
humid = data["Humidity"]
humid_adj = data["HumidityADJ"]


while True: 
    current_status = status_gh(status, humid, humid_adj, temp)
    print("Status in green house: ", status, "Temperature: ", temp, "Humidity: ", humid)
    if current_status == 1:
        relay_dehumid.on()
        relay_mog.on()
        relay_fan.on()
        time.sleep(600)
    elif current_status == 2:
        relay_dehumid.on()
        relay_mog.on()
        relay_fan.off()
        time.sleep(600)
    elif current_status == 3: 
        relay_mog.off()
        relay_fan.on()
        relay_dehumid.on()
        time.sleep(600)
    elif current_status == 4:
        relay_mog.off()
        relay_fan.off()
        relay_dehumid.on()
        time.sleep(600)
    elif current_status == 5:
        relay_mog.on()
        relay_fan.on()
        relay_dehumid.off()
        time.sleep(600)
    elif current_status == 6:
        relay_mog.on()
        relay_fan.off()
        relay_dehumid.off()
        time.sleep(600)

        

