# Eng4-Pi-in-the-Sky

- [Planning](#Planning)
- [Code](#Code)
  - [Payload](#Payload)
  - [Groundhub](#Groundhub) 
- [CAD](#CAD)
  - [Payload](#Payload-1)
  - [Groundhub](#Groundhub-1) 
- [Testing Footage](#Testing-Footage) 
  - [Drop Mechanism](#Drop-Mechanism)
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


### Parts and Uses

| Part                 | Use |
| -------------------- | --- |
| Rasberry Pi Pico     |     |
| Altimeter            |     |
| Foam Padding         |     |
| Helium Balloons      |     |
| #4/40 Nuts and Bolts |     |
| Acrylic              |     |
| PLA                  |     |
| LoRa Radio           |     |
| Phone                |     |
| Wires                |     |
| Servos               |     |
| Resistors            |     |
| Switches             |     |
| LEDs                 |     |
| String               |     |
| Powerboost           |     |
| Battery              |     |

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


## Code

### Payload

The payload didn't have very much necessary code on it, only handling the collecting and sending of altitude data to the ground hub using an altimeter and LoRa transceiver, nd it controls the drop mechanic with a continuous mini servo so that it begins to fall when it reaches the defined maximum altitude. Due to the simplicity of the goals for the payload, the code is fairly straight forward and did not come with many issues. 

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

## CAD

### Payload

Designing the payload, we wanted something that could be opened easily, and that's center of mass would be roughly in the center of the design to avoid problems when flying. We did a circular design with a hinge to split it in half, and used shelves inside to hold the necessary parts. For the design and mechanics of the lift and landing, we made two attachment points for balloons on each side of a center point where we could wrap the string of a balloon around a servo attachment, allowing us to release that balloon remotely, making the payload float back down safely. Our biggest problem was maintaining a low mass, because the heavier the payload is, the more helium is needed to lift it. To solve this, we found spots which could be redesigned to use less material, and we were able to bring down the total weight a large amount. Our final design works well, but there are some ports which are somewhat difficult to use without unscrewing parts.

![Payload Design](https://github.com/jkrosby51/Eng4-Pi-in-the-Sky/blob/d2fedf610a3ad42f0f87dedb114dc86ccf7fb794/images/payloadCAD.png)

### Groundhub

## Testing Footage

### Drop Mechanism

Since we're using balloons to get the payload into the air, we needed to figure out a way to get it back down without it breaking. To do this, we designed a rod that attaches to the servo horn. While some of the balloons will be tied directly to the payload, the strings of some others will be wrapped around this rod. When the payload reaches a certain altitude, the servo will move, which will unwrap the balloons (the released balloons will be tied to a separate string that we'll use to pull them down, similar to a kite). With less balloons attached, the payload should begin to fall. In order to prevent it from breaking upon impact, we will leave enough balloons attached to slow the descent.

Our first test of this mechanism, shown in the video below, was done without balloons. We set a test altitude that is much lower than our final one in order to make sure that it would work properly and fully unwrap the string. We did have to run this test multiple times, since the direction the string is wrapped is important. For the first few tests, we wrapped the string in the same direction the servo rotates, resulting in the payload "eating" it.

https://user-images.githubusercontent.com/56935262/236252742-cf3a1b80-0070-4444-83cb-54d3029338d6.mp4


## To-Do

* get balloons
* document
* figure out number and type of balloons
* fix speaker
* finish groubhub assembly
* attach power switches
* make sure screen works
* final launch
## About Us

### **Josie Muss**

Hey there! I'm Josie, and I'm a member of Charlottesville High School's class of 2023! You can find more of my projects on my [Github](https://github.com/jmuss07). Any questions for me on either this project or any of others that I've worked on can be sent to me at [jmuss07@charlottesvilleschools.org](mailto:jmuss07@charlottesvilleschools.org).
