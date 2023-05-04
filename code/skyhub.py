#type: ignore
#  Wiring/Code References
#1 https://learn.adafruit.com/using-mpl3115a2-with-circuitpython
#2 https://learn.adafruit.com/adafruit-rfm69hcw-and-rfm96-rfm95-rfm98-lora-packet-padio-breakouts/circuitpython-for-rfm9x-lora

import math
import time

import adafruit_mpl3115a2
import adafruit_rfm9x
import board
import busio
import digitalio
import pwmio
from adafruit_motor import servo

### Setting up hardware -- specific pins found on board using pico pin diagram
# Altimeter Setup
sda_pin = board.GP14   
scl_pin = board.GP15       
i2c = busio.I2C(scl_pin, sda_pin)
sensor = adafruit_mpl3115a2.MPL3115A2(i2c)
#

# LoRa Tranceiver Setup
RADIO_FREQ_MHZ = 915.0      # depends on module
CS = digitalio.DigitalInOut(board.GP8)
RESET = digitalio.DigitalInOut(board.GP9)
spi = busio.SPI(clock=board.GP2, MOSI=board.GP3, MISO=board.GP4)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)
rfm9x.tx_power = 23         # adjusts power output, check board for maximum
#

# Continuous Mini Servo Setup
pwm_servo = pwmio.PWMOut(board.GP16, duty_cycle=2 ** 15, frequency=50)  # pulse may need to be tuned to specific servo
servo1 = servo.Servo(pwm_servo, min_pulse=500, max_pulse=2200)
#

altitude_initial = sensor.altitude # sets initial altitude to be starting altitude instead of sea-level
max_altitude = 22           ### in meters, adjust as needed

data = [] # Store height(m) & time(s) data on here as tuples (backup in case ground hub doesnt get data)

while True:
    alt = sensor.altitude - altitude_initial + 1 # sets alt to difference from starting pos in meters
    print(alt)
    data.append((alt,time.monotonic()) #stores data as tuple, (meters from starting pos, fractional seconds). To interperet the time take the difference between data points.
    rfm9x.send(str(alt))     # sends alt as LoRa Packet to be picked up by ground hub
    print(data)
    servo1.angle = 90        # continuous servo stays still
    if int(alt) >= max_altitude:
        servo1.angle = 0     # continuous servo moves counter clockwise
        time.sleep(5)        ### in seconds, adjust delay as needed
        servo1.angle = 90
    
