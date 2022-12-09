#https://learn.adafruit.com/using-mpl3115a2-with-circuitpython

# type: ignore
import board
import digitalio
import time
import math
import pwmio
import busio
import adafruit_mpl3115a2

sda_pin = board.GP16        #UPDATE AS NEEDED
scl_pin = board.GP17        #UPDATE AS NEEDED
i2c = busio.I2C(scl_pin, sda_pin)
sensor = adafruit_mpl3115a2.MPL3115A2(i2c)


sealevel_kPa = 102.29                           ### Find current sea level kPa in Charlottesville here: https://barometricpressure.app/results?lat=38.0386569&lng=-78.4846401
sensor.sealevel_pressure = sealevel_kPa * 1000  ### Manually set sealevel pressure (in Pascals) based on current weather data for more accuracy

while True:

    print('Altitude: {0:0.3f} meters'.format(sensor.altitude))
