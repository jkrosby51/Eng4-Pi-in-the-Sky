# Eng4-Pi-in-the-Sky

- [Planning](#Planning)
  - [Description](#Description)
  - [Timeline](#Timeline)
  - [Materials](#Materials)
  - [Images](#Images)
- [Code](#Code)
  - [Payload](#Payload)
  - [Groundhub](#Groundhub) 
- [CAD](#CAD)
  - [Payload](#Payload-1)
  - [Groundhub](#Groundhub-1) 
- [Wiring Diagrams](#Wiring-Diagrams)
- [Testing Footage](#Testing-Footage) 
  - [Drop Mechanism](#Drop-Mechanism)
- [Reflection](#Reflection)
- [Pictures](#Final-Pictures) 
- [About Us](#About-Us)


## Planning

**Description**: A small robot controlled by a Rasberry Pi will be lifted into the air by helium balloons. As it rises, it will collect altitude data and send messages to a phone that vary based on the detected altitude. Once it reaches a certain altitude, the ballons will drop the robot, which will then enter a state of freefall, safely landing on the ground.

**Test of Success**: The pi will consistently collect altitude data and send it back with the correct message. It will also drop at the correct altitude and land safely/survive.

### What We Need to Learn

- Different versions of design to minimize impact
- Basic app development
- Either Bluetooth or LoRa communication

### Timeline

| Date  | Goal                                                                   |
| ----- | ---------------------------------------------------------------------- |
| 12/9  | Finalize design                                                        |
| 12/16 | Complete non-functional prototype of main design                       |
| 1/13  | Finish a proof of concept of the main code, not connected to mechanics |
| 1/13  | Make prototype of breadboard and mechanics                             |
| 1/20  | Connect code and mechanics, debug                                      |
| 1/27  | Design drop mechanic, start working on app                             |
| 2/03  | Build prototype drop mechanic                                          |
| 2/10  | Assemble full prototype                                                |
| 2/17  | Test protype, have working offline version of app                      |
| 3/03  | Iterative design                                                       |
| 3/10  | Connect app to mechanics and begin app tests                           |
| 3/17  | Balloon tests with none-functioning pay load                           |
| 3/24  | Fall tests                                                             |
| 3/30  | Ready for first test launch                                            |
| 4/14  | Begin test launches                                                    |
| 4/21  | More test launches, fix anything that goes wrong                       |
| 4/28  | Final launch, collect data                                             |
| 5/05  | Analyze data                                                           |
| 5/19  | Finish analyzing data, final documentation, submit project             |


### Materials

* Rasberry Pi Pico
* Metro M4 Airlift Lite
* Prototyping Shield
* MPL3115A2 Altimeter
* RFM9x LoRa
* Helium Balloons
* #4-40 Nuts and Bolts
* #1-72 Nuts and Bolts
* Acrylic
* PLA and ABS
* Wires
* String
* Continuous Servo
* Powerboost and Battery
* String
* 9V battery and Mount
* Locking Power Button
* Power Switch
* 2.8" Adafruit TFT Capacitive Touch Shield
* Male-Female Standoffs
* Perforated Circuit Board

### Safety

- Maintain an open launch/landing area without people or obstacles
- A way to control or limit the horizontal movement during the launch
- Safety equipment during launch
- Safe storage of helium

### Images

**Task Breakdown**

![task breakdown](https://github.com/jkrosby51/Eng4-Pi-in-the-Sky/blob/main/images/maintaskbreakdown.png)

**Code Block Diagram**

![code block diagram](https://github.com/jkrosby51/Eng4-Pi-in-the-Sky/blob/main/images/Engi4.pi-in-the-sky.code-diagram.png)

## Research/Important Information

- https://www.omnicalculator.com/everyday-life/helium-balloons
- [turret voice lines](https://combineoverwiki.net/wiki/Aperture_Science_Sentry_Turret/Quotes)
- [turret sound board](https://www.portal2sounds.com)
- [more turret audios](https://github.com/sourcesounds/portal/tree/master/sound/npc/turret_floor)
- [even more turret audios](https://github.com/sourcesounds/portal2/tree/master/sound/npc/turret)
- [still more turret audios](https://github.com/sourcesounds/portal2/tree/master/sound/npc/turret_floor)
- [SPI guide](https://www.analog.com/en/analog-dialogue/articles/introduction-to-spi-interface.html)


## Code

### Payload

The payload didn't have very much necessary code on it, only handling the collecting and sending of altitude data to the ground hub using an altimeter and LoRa transceiver, and it controls the drop mechanic with a continuous mini servo so that it begins to fall when it reaches the defined maximum altitude. Due to the simplicity of the goals for the payload, the code is fairly straight forward and did not come with many issues. 

The most important section of the code to comment on is the use of the LoRa transceiver as it took some trial and error to get working.
```python3
RADIO_FREQ_MHZ = 915.0      # depends on module
CS = digitalio.DigitalInOut(board.GP8)
RESET = digitalio.DigitalInOut(board.GP9)
spi = busio.SPI(clock=board.GP2, MOSI=board.GP3, MISO=board.GP4)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)
rfm9x.tx_power = 23         # adjusts power output, check board for maximum

rfm9x.send(height)
```
The [Adafruit RFM9x LoRa CircuitPython guide](https://learn.adafruit.com/adafruit-rfm69hcw-and-rfm96-rfm95-rfm98-lora-packet-padio-breakouts/circuitpython-for-rfm9x-lora) was very useful for finding the correct wiring, code, and module details needed to use the RFM9x, along with a basic pico diagram to make sure that the pins we were using would work for specific pin types that the transceiver needed, such as the spi pins. The Radio Frequency (RADIO_FREQ_MHZ) value is specific to the RFM9x, which can use either 868MHz or 915MHz, and the maximum output power (tx_power) value for the module is 23, both of these values were found on the adafruit guide linked above. The rest of the commented code, including setup and usage of the altimeter, mini continuous servo, and data storage linked below.

[Full Code](https://github.com/jkrosby51/Eng4-Pi-in-the-Sky/blob/main/code/skyhub.py)




### Groundhub

The groundhub had a bit more code on it than the payload, since it not only recieved the data transmitted by the payload, but also displayed it on a graph alongside a pre-set message for each altitude. For the LoRa reciever, the [Adafruit RFM9x LoRa CircuitPython guide](https://learn.adafruit.com/adafruit-rfm69hcw-and-rfm96-rfm95-rfm98-lora-packet-padio-breakouts/circuitpython-for-rfm9x-lora) came in handy yet again for the correct wiring, setup, code, and details on how to use the RFM9x. 

When it came to displaying the data, we knew that we wanted to utilize a graph that uptaded over the duration of the flight to do so. However, prior to this project, we had only worked with small OLED screens that would be insufficient forn our intended purposes. This is where the TFT screen came in. While this screen does have touchscreen capabilities, we wanted to use it purely for its size and color display, in order to display the data in a clean way. However, becuase neither of us had used a TFT screen before, it introduced its own unique learning curve and set of challenges. Initially, the problems arose from getting the screen to turn on in the first place. A great resource that was used throughout the process of coding the screen was the CircuitPython portion of the [Adafruit TFT screen guide](https://learn.adafruit.com/adafruit-2-8-tft-touch-shield-v2/circuitpython-displayio-quickstart), as well as the [displayio docs](https://docs.circuitpython.org/en/latest/shared-bindings/displayio/index.html#displayio)! Once the screen was up and running, setting up the axes of the graph was fairly simple. 

After the axes were set up, we had to figure out a way to display our data as the payload sent new data. We created the variables ```altlist``` and ```timelist``` to keep track of the altitudes and their respictive times that would appear on the graph. At the end of the ```while True``` loop, the following code appears to add the newest point to the graph, as well as a line to connect it to the last data point for easier visualization of the flight path, and utilizes the aforementioned ```altlist``` and ```timelist```
```python3
  if currentMeters != lastMeters:
            #creates line to display data! First two parameters are the initial x- and y-positions of the line, and the second two are the final x- and y-positions! The final paramter sets the color of the line
            #timelist[len(timelist)-2] ensures that the new line starts at the x-coordinate of the last point, and altlist[len(altlist-2)] ensures that the new line starts at the y-coordinate of the last point
            #any time a part of timelist is called, it must be added to xPixel in order to create the line with respect to the origin of the graph, and whenever a part of altlist is called, it must be subtracted from yPixel for the same reason
            #The second pair of x- and y-coordinates are written with timelist[i+1] and altlist[i+1] respectively to ensure that the line will end at the next data point
            #timelist is multiplied by 3 and altlist is multiplied by 18 in order to scale the graph to be visible and large enough to distinguish individual data points
            line = Line((xPixel+3*timelist[len(timelist)-2]), (yPixel-18*altlist[len(altlist)-2]), (xPixel+3*timelist[len(timelist)-1]), (yPixel-18*altlist[len(timelist)-1]), color=0xff5d00)
            splash.append(line)

            #The first two parameters center the circle around the data point at the end of the last graphed line
            circle = Circle(xPixel+3*(timelist[len(timelist)-1]), yPixel-18*(altlist[len(altlist)-1]), 2, fill=0x0065ff, outline=0x0065ff)
            splash.append(circle)
            point_label = displayio.Group(scale=1, x=(xPixel+timelist[len(timelist)-1]-10), y=(yPixel-18*(altlist[len(altlist)-1])-8)) #sets font, size, and start position of message
            point = f"({timelist[len(timelist)-1]}, {altlist[len(timelist)-1]})" #makes an f-string with showing the coordinates; these coordinates are defined by the last thing in timelist and altlist
            text_area = label.Label(coord_font, text=point, color=0x470400) #adds coordinate text to display group
            point_label.append(text_area)  #subgroup for text scaling
            splash.append(point_label) #adds to splash
            
        if len(altlist) > 8:
            break #breaks out of the else statement to stop graphing and avoid memory error after collecting the desired number of data points
```

We knew from the start that we wanted the grounhub to play some kind of message that would correspond to altitudes certain distances apart. While we initially planned to do this using a soundboard and speaker, it stopped working in the final stretch of the project, forcing us to scrap the system. However, instead of doing away with the messages all together, we made it so that it would be written on the screen, and maintained the changing aspect of it. Both the speaker and the written form used the same base code, which is displayed below! 

```python3
if currentMeters >= 7:
            descending = True #changes value of "descending" to indicate that the payload is now descending; only happens once it reaches its maximum altitude of seven meters
            
        #Compares the current altitude value recieved by the LoRa with the last graphed altitude (note! the last graphed altitude is not the same as the last recieved altitude!) 
        #If this value is greater than or equal to 1 and the payload is ascending, continue
        if (currentMeters - lastMeters) >= 1 and descending == False:
            msg_area.msg = upmessage_array[int(currentMeters/3)] #changes the message text displayed to appropriate one from array
            
            altlist.append(currentMeters) #adds the current altitude to altlist
            timelist.append(int(time.monotonic() - start_time)) #finds the current time elapsed by subtracting time.monotonic from the start time, and adds it to timelist
            lastMeters = currentMeters #sets lastMeters equal to currentMeters, making it the new last graphed time
        
        #Only do this if the payload is descending! The distance between lastMeters and currentMeters is not needed here
        if descending == True:
            msg_area.msg = downmessage_array[0] #changes the message text displayed to appropriate one from array
            time.sleep(2) #waits two seconds
            msg_area.msg = downmessage_array[1] #changes the message text displayed to appropriate one from array
            
            altlist.append(currentMeters)  #adds the current altitude to altlist
            timelist.append(int(time.monotonic() - start_time)) #finds the current time elapsed by subtracting time.monotonic from the start time, and adds it to timelist
            lastMeters = currentMeters #sets lastMeters equal to currentMeters, making it the new last graphed time
```

The entirety of the commented code for the groundhub can be found [here](https://github.com/jkrosby51/Eng4-Pi-in-the-Sky/blob/main/code/groundhub.py)

## CAD

### Payload

Designing the payload, we wanted something that could be opened easily, and thats center of mass would be roughly in the center of the design to avoid problems when flying. We did a circular design with a hinge to split it in half, and used shelves inside to hold the necessary parts. For the design and mechanics of the lift and landing, we made two attachment points for balloons on each side of a center point where we could wrap the string of a balloon around a servo attachment, allowing us to release that balloon remotely, making the payload float back down safely. Our biggest problem was maintaining a low mass, because the heavier the payload is, the more helium is needed to lift it. To solve this, we found spots which could be redesigned to use less material, and we were able to bring down the total weight a large amount. Our final design works well, but there are some ports which are somewhat difficult to use without unscrewing parts.

![Payload Design](https://github.com/jkrosby51/Eng4-Pi-in-the-Sky/blob/d2fedf610a3ad42f0f87dedb114dc86ccf7fb794/images/payloadCAD.png)

### Groundhub

While the code for the groundhub was more complex, the CAD felt fairly simple. Because the groundhub was not meant to enter the air, it's weight, aerodynamics, and survivability did not influence our design. Instead, we went into the project with the idea of making a groundhub that looked like an old Gameboy, a design that we stuck with. We included fake buttons and a d-pad that are attached to springs that sit in a housing within the groundhub. However, one of these buttons was later replaced with a locking pushbutton that serves as the power button. Designing the casing itself went fairly smoothly, apart from our use of improper measurements of the TFT screen. Not only did we design the hole for the screen to be too small in both width and height, it was also made too deep, which made it so that we could not properly secure the front of the casing to the back plate; instead of lying flush as intended, the inner edge of the hole's lip banged against both our wires, as well as the screen, Metro, and prototyping shield. Due to the large amount of print material used to create the shell of the groundhub, we didn't want to print out a new one with just a few small changes made to it, so we took a dremel and sand paper to the inside edges instead and cut it down to size.

![Groundhub Design](https://github.com/jkrosby51/Eng4-Pi-in-the-Sky/blob/main/images/groundhubCAD.png)

## Wiring Diagrams

### Payload Wiring

![Payload Wiring](https://github.com/jkrosby51/Eng4-Pi-in-the-Sky/blob/main/images/payload%20wiring%20diagram.png?raw=true)

### Groundhub Wiring

![Groundhub Wiring](https://github.com/jkrosby51/Eng4-Pi-in-the-Sky/blob/main/images/groundhub%20wiring%20diagram.png?raw=true)

## Testing Footage

### Drop Mechanism

Since we're using balloons to get the payload into the air, we needed to figure out a way to get it back down without it breaking. To do this, we designed a rod that attaches to the servo horn. While some of the balloons will be tied directly to the payload, the strings of some others will be wrapped around this rod. When the payload reaches a certain altitude, the servo will move, which will unwrap the balloons (the released balloons will be tied to a separate string that we'll use to pull them down, similar to a kite). With less balloons attached, the payload should begin to fall. In order to prevent it from breaking upon impact, we will leave enough balloons attached to slow the descent.

Our first test of this mechanism, shown in the video below, was done without balloons. We set a test altitude that is much lower than our final one in order to make sure that it would work properly and fully unwrap the string. We did have to run this test multiple times, since the direction the string is wrapped is important. For the first few tests, we wrapped the string in the same direction the servo rotates, resulting in the payload "eating" it.

https://user-images.githubusercontent.com/56935262/236252742-cf3a1b80-0070-4444-83cb-54d3029338d6.mp4


## Reflection
Unfortunately, with a week left before the project's due date, we ran into several roadblocks. Our plan for launch was to use balloons to lift our payload into the air. Unfortunately, the sources we used to calculate how many balloons would be needed to the payload were incorrect, and we did not purchase nearly enough balloons to lift even an inch above the ground, let alone attain the desired altitude. Due to this occuring so close to the finish line, we were forced to scrap our original plan, instead attaching the altimiter and LoRa boards to a phone-operated drone. We were also unaware that the Pico sending data back to a groundhub was not sufficient for data collection, and we had to scramble to introduce an on-board data storage system to the Pico at the last minute. By the due date for launching, onboard storage was failing to properly write data, and the ground hub had it's own new issue. We unfortunately didn't have time to figure out the cause of those issues and so were unable to launch in time. Some of the main reasons for this was scope creep and poor prioritization, as we worked on non-essential parts of the project before finishing some essential parts which seemed easy to complete but turned out to cause more issues than anticipated. Some of these non-essential parts were also scrapped even after lots of time was put into it because issues came up which we weren't able to solve. Overall, to be more successful, we should have focused on making the flight and data collection work, and then add the fancy stuff afterwards.

## Final Pictures

### Payload

<img src="https://github.com/jkrosby51/Eng4-Pi-in-the-Sky/blob/main/images/PayloadImage1.jpg" width="437" height="487">

<img src="https://github.com/jkrosby51/Eng4-Pi-in-the-Sky/blob/main/images/PayloadImage2.jpg" width="582" height="487">

### Groundhub

<img src="https://github.com/jkrosby51/Eng4-Pi-in-the-Sky/blob/main/images/groundhub_1.jpg?raw=true" width="254" height="327">

<img src="https://github.com/jkrosby51/Eng4-Pi-in-the-Sky/blob/main/images/groundhub_2.jpg?raw=true" width="300" height="347">

<img src="https://github.com/jkrosby51/Eng4-Pi-in-the-Sky/blob/main/images/groundhub_3.jpg?raw=true" width="419" height="576">

## About Us

### **Josie Muss**

Hey there! I'm Josie, and I'm a member of Charlottesville High School's class of 2023! You can find more of my projects on my [Github](https://github.com/jmuss07). Any questions for me on either this project or any of others that I've worked on can be sent to me at [jmuss07@charlottesvilleschools.org](mailto:jmuss07@charlottesvilleschools.org).
