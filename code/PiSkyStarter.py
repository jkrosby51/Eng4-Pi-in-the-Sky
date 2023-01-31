#type: ignore
# https://learn.adafruit.com/using-mpl3115a2-with-circuitpython
# https://www.tomshardware.com/how-to/get-wi-fi-internet-on-raspberry-pi-pico
# https://www.howtoforge.com/using-an-android-smartphone-as-a-wlan-hotspot

import math
import time
import adafruit_mpl3115a2
import board
import busio
import digitalio
import pwmio
import adafruit_rfm9x
from adafruit_motor import servo

sda_pin = board.GP14        #UPDATE AS NEEDED
scl_pin = board.GP15        #UPDATE AS NEEDED
i2c = busio.I2C(scl_pin, sda_pin)
sensor = adafruit_mpl3115a2.MPL3115A2(i2c)

RADIO_FREQ_MHZ = 915.0
CS = digitalio.DigitalInOut(board.GP17)
RESET = digitalio.DigitalInOut(board.GP16)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)
rfm9x.tx_power = 23

pwm_servo = pwmio.PWMOut(board.GP2, duty_cycle=2 ** 15, frequency=50)  # pulse may need to be tuned to specific servo
servo1 = servo.Servo(pwm_servo, min_pulse=500, max_pulse=2200)

#sealevel_Pa = 102290                           ### Find current sea level kPa in Charlottesville here: https://barometricpressure.app/results?lat=38.0386569&lng=-78.4846401
sensor.sealevel_pressure =  sealevel_Pa         ### Manually set sealevel pressure (in Pascals) based on current weather data for more accuracy
altitude_initial = sensor.altitude #sets initial altitude to be starting altitude instead of sea-level
max_altitude = 22 #temporary value

while True:
    rfm9x.send(sensor.altitude)

    if int(sensor.altitude) == max_altitude:
        servo1.angle = 0                        ### figure out the exact angle later
