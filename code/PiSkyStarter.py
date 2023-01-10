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
max_altitude = 22 #temporary value

msg1 = ["helloo!", "n"] # turret_autosearch_1
msg2 = ["put me down!", "n"] # turret_pickup_2
msg3 = ["who are you?", "n"] # turret_pickup_5
msg4 = ["help", "n"] # turret _pickup_8
msg5 = ["are you still there?", "n"] # turret_search_1
msg6 = ["no hard feelings", "n"] # turret_disabled_8
msg7 = ["whyyyy", "n"] # turret_disabled_7
msg8 = ["i dont blame you", "n"] # turret_disabled_5
msg9 = ["my fault", 'n'] # turret_collide_4
msg10 = ["goodnight", "n"] # turret_retire_5
msg11 = ["aaaaaaaaa", "n"] #turret_fizzler_1

'''
other potential voice lines:
- turret_tipped_5
- sp_sabotage_factory_good_fail02
- sp_sabotage_factory_good_fail03
- sp_sabotage_factory_good_fail05
- sp_sabotage_factory_good_fail06
- turretlaunched01
- turretlaunched02
- turretlaunched03
- turretlaunched05
- turretlaunched06
- turretlaunched07
- turretlaunched10
- turretlightbridgeblock02
- turretlightbridgeblock03
- turretshotbylaser07
- turretshotbylaser08
- turretstuckintubetakemewith01
- turretstuckintubegoodbye01
- turretstuckintubetakemewith02
- turretwitnessdeath11
- turret_tipped_6
- turretstuckintube09
- turret_autosearch_1
- turret_pickup_2
- turret_pickup_5
- turret_pickup_8
- turret_search_1
- turret_disabled_8
- turret_disabled_7
- turret_disabled_5
- turret_collide_4
- turret_retire_5
- turret_fizzler_1
- turretlaunched09
- turretlaunched08
- sp_sabotage_factory_good_fail04

'''
#see also "weeeeee - OHNO" "Im flying!" for message 11


while True:

    print(f"Altitude: {sensor.altitude} meters")
    
    if (sensor.altitude - altitude_initial) > 0 and (sensor.altitude - altitude_initial) < 2 and message1[1] == "n": #temporary altitude values
        print message1[0]
        message1[1] = "y"
        
    if (sensor.altitude - altitude_initial) > 2 and (sensor.altitude - altitude_initial) < 4 and message2[1] == "n": #temporary altitude values
        print message2[0]
        message2[1] = "y"
        
    if (sensor.altitude - altitude_initial) > 4 and (sensor.altitude - altitude_initial) < 6 and message3[1] == "n": #temporary altitude values
        print message3[0]
        message3[1] = "y"
        
    if (sensor.altitude - altitude_initial) > 6 and (sensor.altitude - altitude_initial) < 8 and message4[1] == "n": #temporary altitude values
        print message4[0]
        message4[1] = "y"
        
    if (sensor.altitude - altitude_initial) > 8 and (sensor.altitude - altitude_initial) < 10 and message5[1] == "n": #temporary altitude values
        print message5[0]
        message5[1] = "y"
        
    if (sensor.altitude - altitude_initial) > 10 and (sensor.altitude - altitude_initial) < 12 and message6[1] == "n": #temporary altitude values
        print message6[0]
        message6[1] = "y"
        
    if (sensor.altitude - altitude_initial) > 12 and (sensor.altitude - altitude_initial) < 14 and message7[1] == "n": #temporary altitude values
        print message7[0]
        message7[1] = "y"
        
    if (sensor.altitude - altitude_initial) > 14 and (sensor.altitude - altitude_initial) < 16 and message8[1] == "n": #temporary altitude values
        print message8[0]
        message8
        [1] = "y"
        
    if (sensor.altitude - altitude_initial) > 16 and (sensor.altitude - altitude_initial) < 18 and message9[1] == "n": #temporary altitude values
        print message9[0]
        message9[1] = "y"
        
    if (sensor.altitude - altitude_initial) > 18 and (sensor.altitude - altitude_initial) < 20 and message10[1] == "n": #temporary altitude values
        print message10[0]
        message10[1] = "y"
    