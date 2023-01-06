# https://learn.adafruit.com/using-mpl3115a2-with-circuitpython
# https://www.tomshardware.com/how-to/get-wi-fi-internet-on-raspberry-pi-pico
# https://www.howtoforge.com/using-an-android-smartphone-as-a-wlan-hotspot

# type: ignore
import board
import digitalio
import time
import math
import pwmio
import busio
import adafruit_mpl3115a2

sda_pin = board.GP14        #UPDATE AS NEEDED
scl_pin = board.GP15        #UPDATE AS NEEDED
i2c = busio.I2C(scl_pin, sda_pin)
sensor = adafruit_mpl3115a2.MPL3115A2(i2c)


sealevel_Pa = 102290                           ### Find current sea level kPa in Charlottesville here: https://barometricpressure.app/results?lat=38.0386569&lng=-78.4846401
sensor.sealevel_pressure = sealevel_Pa         ### Manually set sealevel pressure (in Pascals) based on current weather data for more accuracy
altitude_initial = sensor.altitude #sets initial altitude to be starting altitude instead of sea-level

msg1 = ["helloo!", "n"]
msg2 = ["put me down!", "n"]
msg3 = ["who are you?", "n"]
msg4 = ["help", "n"]
msg5 = ["are you still there?", "n"]
msg6 = ["no hard feelings", "n"]
msg7 = ["whyyyy", "n"]
msg8 = ["i dont blame you", "n"]
msg9 = ["my fault", 'n']
msg10 = ["goodnight", "n"]
msg11 = ["aaaaaaaaa", "n"]


while True:

    print(f"Altitude: {sensor.altitude} meters")
