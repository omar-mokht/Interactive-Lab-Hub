   
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
bigfont = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 100)

# smallfont = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 50)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# if disp.rotation % 180 == 90:
#     height = disp.width  # we swap height/width to rotate it to landscape!
#     width = disp.height
# else:
#     width = disp.width  # we swap height/width to rotate it to landscape!
#     height = disp.height
# image = Image.new("RGB", (width, height))

# draw = ImageDraw.Draw(image)

# # Draw a black filled box to clear the image.
# draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
# disp.image(image)

# image = Image.open("red.jpg")

# image_ratio = image.width / image.height
# screen_ratio = width / height
# if screen_ratio < image_ratio:
#     scaled_width = image.width * height // image.height
#     scaled_height = height
# else:
#     scaled_width = width
#     scaled_height = image.height * width // image.width
# image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

# # Crop and center the image
# x = scaled_width // 2 - width // 2
# y = scaled_height // 2 - height // 2
# image = image.crop((x, y, x + width, y + height))

dotx = 0
doty = 0
dir = 1
seconds = 0
incrementx = width/10
incrementy = height/6
doty = -incrementy
while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0,fill=(0,0,0))
    # y = (top+bottom)/3
    # incrementx = width/10
    # incrementy = height/6
    # dotx -= incrementx
    # draw.text((x,y),strftime("%m/%d/%Y %H:%M:%S"), end="", flush=True, font=font, fill="#FFFFFF")
    # # Display image.
    if not buttonA.value:
        seconds = 0
        dotx = 0
        doty = 0
        dir = 1
        seconds = 0
        incrementx = width/10
        incrementy = height/6
        doty = -incrementy
    draw.text((dotx,doty), ".",font=font, fill="#FFFFFF" )
    if dotx >= width:
        doty += incrementy
        dotx = 0
    if seconds % 10 == 0:
        # print("hi")
        # draw.rectangle((0, 0, width, height), outline=0,fill=400)
        draw.rectangle((0, 0, width, height), outline=0,fill = (0,0,0))

        draw.text((width/3+20,height/3), str(seconds), font=font, fill="#00FF00")
        # time.sleep(1)
    if seconds == 60:
        seconds = 0
        dotx = 0
        doty = 0
        dir = 1
        seconds = 0
        incrementx = width/10
        incrementy = height/6
        doty = -incrementy

    seconds +=1
    # if doty >= height-incrementy:
    #     doty = 0
        # dotx = 0
    print(str(dotx) + "," + str(doty))
    dotx += incrementx
    disp.image(image, rotation)
    time.sleep(0.1)

   
   
   
    #TODO: Lab 2 part D work should be filled in here. You should be able to look in cli_clock.py and stats.py 
    # t = time.strftime("%H:%M:%S")
    # hour, m, sec = t.split(':')
    # hour = int(hour)
    # tmin = hour * 60 + int(m)
    # colval = int(255 - 255/720 * (abs(720 - tmin)))
    # if buttonB.value and not buttonA.value:  # just button A pressed
    #     draw.text((x, top), t, font=font, fill="#FFFFFF")
    # if buttonA.value and not buttonB.value:  # just button B pressed
    #     rtmin = random.randint(0, 1439)
    #     colval = int(255 - 255/720 * (abs(720 - rtmin)))
    #     draw.rectangle((0, 0, width, height), outline=0, fill=(colval, colval, colval))
    #     draw.text((x, top), str(rtmin), font=font, fill="#FFFFFF")
    #     time.sleep(1)
    # if buttonA.value and buttonB.value: #nothing is pressed
    #     #display color
    #     draw.rectangle((0, 0, width, height), outline=0, fill=(colval, colval, colval))
    #     draw.text((x, (top + bottom) / 2), str(t), font=font, fill="#FFFFFF")