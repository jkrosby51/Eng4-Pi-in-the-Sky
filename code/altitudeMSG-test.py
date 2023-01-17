
messagePin = #array full of pins! wait- is that a real thing?

startMeters = int(sensor.altitude)
lastMeters = startMeters
while True:
    currentMeters = int(sensor.altitude - startMeters)
    if currentMeters/3 != lastMeters/3:
        currentPin = digitalio.DigitalInOut(messagePin[currentMeters])
        currentPin.direction = digitalio.Direction.OUTPUT
        currentPin = True #or is it false?? idk
        time.sleep(.5)
        currentPin = False
