   
import time
import subprocess
import digitalio
import board
from time import strftime, sleep
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import random

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
smallfont = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)


# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()



dotx = 0
doty = 0
dir = 1
seconds = 0
incrementx = width/10
incrementy = height/6
while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0,fill=(0,0,0))
    if not buttonA.value:
        seconds = 0
        dotx = 0
        doty = 0
        incrementx = width/10
        incrementy = height/6
    draw.text((dotx,doty), "T",font=smallfont, fill="#FFFFFF" )
    if dotx >= width:
        doty += incrementy
        dotx = 0
    if seconds % 10 == 0:
        draw.rectangle((0, 0, width, height), outline=0,fill = (0,0,0))
        draw.text((width/3+20,height/3), str(seconds), font=font, fill="#00FF00")
    if seconds == 60:
        seconds = 0
        dotx = 0
        doty = 0
        dir = 1
        seconds = 0
        incrementx = width/10
        incrementy = height/6
    seconds +=1
    dotx += incrementx
    disp.image(image, rotation)
    time.sleep(1)