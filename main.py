from machine import Pin, PWM
import network
import time
import urequests

# -----------------------------
# PIN CONFIGURATION
# -----------------------------

pir = Pin(13, Pin.IN)

servo = PWM(Pin(14))
servo.freq(50)

# -----------------------------
# THINGSPEAK SETTINGS
# -----------------------------

WRITE_API_KEY = "YOUR_WRITE_API_KEY"
THINGSPEAK_URL = "https://api.thingspeak.com/update"

# -----------------------------
# SERVO FUNCTION
# -----------------------------

def set_angle(angle):
    duty = int(40 + (angle / 180) * 75)
    servo.duty(duty)

# Door initially closed
set_angle(0)

# -----------------------------
# CONNECT TO WIFI
# -----------------------------

print("Connecting to WiFi...")

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect("Wokwi-GUEST", "")

while not wifi.isconnected():
    print(".", end="")
    time.sleep(0.5)

print()
print("WiFi connected!")
print(wifi.ifconfig())

# -----------------------------
# SEND DATA TO THINGSPEAK
# -----------------------------

def send_to_thingspeak(motion):
    url = THINGSPEAK_URL
    url += "?api_key=" + WRITE_API_KEY
    url += "&field1=" + str(motion)

    try:
        response = urequests.get(url)
        print("ThingSpeak response:", response.text)
        response.close()

    except Exception as e:
        print("ThingSpeak error:", e)

# -----------------------------
# MAIN PROGRAM
# -----------------------------

last_motion = -1

while True:

    motion = pir.value()

    if motion == 1:

        print("Motion detected")
        print("Door opening")

        set_angle(90)

        if last_motion != 1:
            send_to_thingspeak(1)
            last_motion = 1

        time.sleep(3)

        print("Door closing")
        set_angle(0)

    else:

        print("No motion")

        if last_motion != 0:
            send_to_thingspeak(0)
            last_motion = 0

    time.sleep(2)
