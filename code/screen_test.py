import board
import terminalio
import displayio
from adafruit_display_text import label
from adafruit_display_shapes.line import Line
from adafruit_display_shapes.rect import Rect
import adafruit_ili9341
displayio.release_displays() #set up for screen by releasing all used pins for new display
# Use Hardware SPI
spi = board.SPI()

tft_cs = board.D10
tft_dc = board.D9

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = adafruit_ili9341.ILI9341(display_bus, width=320, height=240)

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

yPixel = 160 #origin of graph
xPixel = 40 #origin of graph

while True:
    pass