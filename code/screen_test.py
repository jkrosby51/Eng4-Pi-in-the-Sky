import adafruit_ili9341
import time
import board
import displayio
import terminalio
import busio
from adafruit_display_shapes.line import Line
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

displayio.release_displays() #set up for screen by releasing all used pins for new display

spi = busio.SPI(clock=board.D13, MOSI=board.D11, MISO=board.D12)

tft_cs = board.D10
tft_dc = board.D9

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = adafruit_ili9341.ILI9341(display_bus, width=320, height=240, rotation=180)

# Make the display context
splash = displayio.Group()
display.show(splash)

# Draw a green background
color_bitmap = displayio.Bitmap(320, 240, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xAFAFAF  #grey

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)

splash.append(bg_sprite)


# Make the graph's axes
hRect = Rect(40, 200, 240, 2, fill=0x470400)#sets start coordinates, width, height, and fill color of the line serving as the x-axis
splash.append(hRect) #adds to splash

vRect = Rect(40, 40, 2, 160, fill=0x470400) #sets start coordinates, width, height, and fill color of the line serving as the y-axis
splash.append(vRect) #adds to splash

#makes a custom font to use for the coordinate labels
coord_font = bitmap_font.load_font("/lib/JosefinSans-Bold-10.bdf")

### My science teacher said we have to label the axes!!!!! pls add >:(

#label the x-axis
text_group = displayio.Group(scale=1, x=240, y=210) #sets size and start position of message
text = "time(s)"
text_area = label.Label(terminalio.FONT, text=text, color=0x470400) #adds text to label x-axis to display group
text_group.append(text_area)  #subgroup for text scaling
splash.append(text_group) #adds to splash

#label the y-axis
text_group = displayio.Group(scale=1, x=3, y=45) #sets size and start position of message
text = "alt(m)"
text_area = label.Label(terminalio.FONT, text=text, color=0x470400) #adds text to label y-axis to display group
text_group.append(text_area)  #subgroup for text scaling
splash.append(text_group) #adds to splash

yPixel = 200 #origin of graph
xPixel = 40 #origin of graph


start_time = time.monotonic()
altlist = [0] #creates list of altitudes
timelist = [0] #creates list of times
count = [0, 1, 2, 3, 4, 5, 6, 7, 0]

#list of messages to use
message_array = ["Hellooo!", "Put me down!", "What are you doing?", "Help!", "Thanks anyway...", "I'm scared...", "AHHHHHHHHH!", "I'm flyinnnng!"]
        
#display message!
message_text = displayio.Group(scale=2, x=5, y=220) #sets size and start position of message
text = message_array[4] #chooses the appropriate message from the array and sets it as the text
text_area = label.Label(terminalio.FONT, text=text, color=0x470400) #adds text to label y-axis to display group
message_text.append(text_area)  #subgroup for text scaling
splash.append(message_text) #adds to splash
'''
for i in range(len(timelist)-1): #is that syntax correct for range()? -------------------------CHECK
    #creates line to display data! First two parameters are the initial x- and y-positions of the line, and the second two are the final x- and y-positions! This final paramter sets the color of the line
    #timelist[i] must be added to xPixel in order to create the line with respect to the origin of the graph, and altlist[i] must be subtracted from yPixel for the same reason
    #The second pair of x- and y-coordinates are written with timelist[i+1] and altlist[i+1] respectively to ensure that the line will end at the next data point
    #timelist is multiplied by 3 and altlist is multiplied by 10 in order to scale the graph to be visible and large enough to distinguish individual data points
    line = Line(xPixel+3*(timelist[i]), yPixel-18*(altlist[i]), xPixel+3*(timelist[i+1]), yPixel-18*(altlist[i+1]), color=0xff5d00)
    splash.append(line)
    #The first two parameters center the circle around the data point at the end of the last graphed line
    circle = Circle(xPixel+3*(timelist[i+1]), yPixel-18*(altlist[i+1]), 2, fill=0x0065ff, outline=0x0065ff)
    splash.append(circle)
    point_label = displayio.Group(scale=1, x=(xPixel+3*(timelist[i+1])-10), y=(yPixel-18*(altlist[i+1])-8)) #sets size and start position of message
    point = f"({timelist[i]}, {altlist[i]})" #chooses the appropriate message from the array and sets it as the text
    text_area = label.Label(coord_font, text=point, color=0x470400) #adds text to label y-axis to display group
    point_label.append(text_area)  #subgroup for text scaling
    splash.append(point_label) #adds to splash
    '''
while True:
    for i in range(len(count)):
        altlist.append(i)
        timelist.append(i)
        line = Line(xPixel+3*timelist[len(timelist)-2], yPixel-18*altlist[len(altlist)-2], xPixel+3*timelist[len(timelist)-1], yPixel-18*altlist[len(timelist)-1], color=0xff5d00)
        splash.append(line)
        #The first two parameters center the circle around the data point at the end of the last graphed line
        circle = Circle(xPixel+3*(timelist[len(timelist)-1]), yPixel-18*(altlist[len(altlist)-1]), 2, fill=0x0065ff, outline=0x0065ff)
        splash.append(circle)
        point_label = displayio.Group(scale=1, x=(xPixel+timelist[len(timelist)-1]-10), y=((yPixel-18*(altlist[len(altlist)-1])-8))) #sets font, size, and start position of message
        point = f"({timelist[len(timelist)-1]}, {altlist[len(timelist)-1]})" #makes an f-string with showing the coordinates; these coordinates are defined by the last thing in timelist and altlist
        text_area = label.Label(coord_font, text=point, color=0x470400) #adds coordinate text to display group
        point_label.append(text_area)  #subgroup for text scaling
        splash.append(point_label) #adds to splash
    
    if len(altlist) > 9:
        break #breaks out of while True loop to stop graphing and avoid memory error after collecting the desired number of data points
while True:
    pass #enters new empty loop to freeze screen on final graph