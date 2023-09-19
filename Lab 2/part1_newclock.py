import time
from time import strftime, sleep
from datetime import datetime
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

# Planetary Clock
# Author: Yifan Zhou
# 09/10/2023
# yz2889@cornell.edu

# Assume a Starting date 'YYYY-MM-DD HH:MM:SS'
zero_date_str = '2000-01-01 00:00:00'
# Convert the zero date string to a datetime object
zero_date = datetime.strptime(zero_date_str, '%Y-%m-%d %H:%M:%S')

# List of planets
planets = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']

# Listing day length in seconds for every planet:
Planet_Day_Durations = {
    'Mercury': 5155200,    # Approximately 59 Earth days and 16 hours
    'Venus': 20995200,     # Approximately 243 Earth days
    'Earth': 86400,         # 24 hours
    'Mars': 88620,          # Approximately 24 hours and 37 minutes
    'Jupiter': 35700,       # Approximately 9 hours and 55 minutes
    'Saturn': 38000,        # Approximately 10 hours and 33 minutes
    'Uranus': 61884,        # Approximately 17 hours and 14 minutes
    'Neptune': 57996        # Approximately 16 hours and 6 minutes
}

# Listing day length in hour+minutes
Planet_Day_Durations_Hours_Minutes = {
    'Mercury': (1476, 0),      # Approximately 59 Earth days and 16 hours
    'Venus': (5832, 0),        # Approximately 243 Earth days
    'Earth': (24, 0),          # 24 hours
    'Mars': (24, 37),          # Approximately 24 hours and 37 minutes
    'Jupiter': (9, 55),       # Approximately 9 hours and 55 minutes
    'Saturn': (10, 33),       # Approximately 10 hours and 33 minutes
    'Uranus': (17, 14),       # Approximately 17 hours and 14 minutes
    'Neptune': (16, 6)        # Approximately 16 hours and 6 minutes
}

# Planet display theme colors:
Planet_Text_Colors = {
    'Mercury': "#E6DCB2",    
    'Venus': "#F2D9A3",    
    'Earth': "#FFFFFF",         
    'Mars': "#F26868",          
    'Jupiter': "#F2D9A3",      
    'Saturn': "#F7DF4F",       
    'Uranus': "#9BFEFA",       
    'Neptune': "#4DA1ED"       
}


# This function will return current time on each planet 
# in exact hour/minute/seconds
# in the form of a tuple (hour, minute, seconds)
def get_current_planet_time_exact(planet_id):
    # Get the current date and time
    current_date = datetime.now()

    # Calculate the time difference 
    time_difference = current_date - zero_date

    # Extract the total elapsed seconds of current day
    elapsed_seconds = time_difference.total_seconds() % Planet_Day_Durations[planets[planet_id]]
    
    # Extract current hour
    hours = elapsed_seconds // 3600
    seconds_remainder = elapsed_seconds % 3600
    
    # Extract current minutes
    minutes = seconds_remainder // 60
    
    # Extract current secnods
    seconds = seconds_remainder % 60
    
    return tuple(int(x) for x in (hours, minutes, seconds))
    

# This function will return current time on each planet 
# scaled to earth 24 hour range
# in the form of a tuple (hour, minute, seconds)
def get_current_planet_time_scaled(planet_id):
    # Get the current date and time
    current_date = datetime.now()

    # Calculate the time difference 
    time_difference = current_date - zero_date

    # Extract the total elapsed seconds of current day
    elapsed_seconds = time_difference.total_seconds() % Planet_Day_Durations[planets[planet_id]]
    
    # scale the current seconds into "seconds" for that planet
    elapsed_seconds = elapsed_seconds * (86400 / Planet_Day_Durations[planets[planet_id]])
    
    # Extract current hour
    hours = elapsed_seconds // 3600
    seconds_remainder = elapsed_seconds % 3600
    
    # Extract current minutes
    minutes = seconds_remainder // 60
    
    # Extract current secnods
    seconds = seconds_remainder % 60
    
    return tuple(int(x) for x in (hours, minutes, seconds))


# Button configuration
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

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

# Prepare Fonts
Sans = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
Sans_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf", 35)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

def transition(id):
    prev_id = len(planets) - 1 if current_id == 0 else current_id - 1
    prev_x = -95
    current_x = 255
    # load the two images
    background_image = Image.open(f'img/background.png')
    planet_image = Image.open(f'img/{planets[current_id]}.png')
    prev_planet_image = Image.open(f'img/{planets[prev_id]}.png')
    while current_x >= -95:
        # paint background
        image.paste(background_image, (0, 0))
        # put the planet in the foreground
        image.paste(planet_image, (current_x, 0), planet_image)
        image.paste(prev_planet_image, (prev_x, 0), prev_planet_image)
        
        disp.image(image, rotation)
        
        # current_x -= 50
        # prev_x -= 50
        current_x -= int( (current_x - (-95)) * 2/5 )
        prev_x -= int( (current_x - (-95)) * 2/5 )
        
        if int( (current_x - (-95)) * 2/5 ) < 2:
            break
        sleep(0.05)
    

current_id = 2 # By default we start from Earth at index 2
time_text_xy = [75, 40] 
planet_img_xy = [-95, 0]
planet_img_size = []
while(1):
    # Use bottonA to switch to the next planet time
    if not buttonA.value:
        current_id += 1
        if current_id >= len(planets):
            current_id = 0
            
        # play transition animation
        transition(current_id)
        while not buttonA.value:
            pass
    
    # Hold down bottonB to view unscaled time
    if not buttonB.value:
        # load the two images
        background_image = Image.open(f'img/background.png')
        planet_image = Image.open(f'img/{planets[current_id]}.png')
        
        current_y = 0
        while not buttonB.value:
            # Morph to exact time View
            # paint background
            image.paste(background_image, (0, 0))
            # put the planet in the foreground
            image.paste(planet_image, (-95, current_y), planet_image)
            if current_y == 40:
                # Place text
                time_exact = get_current_planet_time_exact(current_id)
                draw.text((10, 10), f'{time_exact[0]}:{time_exact[1]}:{time_exact[2]}', font=Sans_bold, fill=Planet_Text_Colors[planets[current_id]])
                draw.text((85, 50), "Exact Time:", font=Sans, fill=Planet_Text_Colors[planets[current_id]])
                draw.text((85, 70), f'{Planet_Day_Durations_Hours_Minutes[planets[current_id]][0]} hr {Planet_Day_Durations_Hours_Minutes[planets[current_id]][1]} min \nper day', font=Sans, fill=Planet_Text_Colors[planets[current_id]])
            else:
                current_y += 8
            
            disp.image(image, rotation)
            sleep(0.05)
            
        # Morph back to scaled time view
        while current_y >= 0:
            # paint background
            image.paste(background_image, (0, 0))
            # put the planet in the foreground
            image.paste(planet_image, (-95, current_y), planet_image)
            
            current_y -= 8
            disp.image(image, rotation)
            sleep(0.05)
    
    # load the two images
    background_image = Image.open(f'img/background.png')
    planet_image = Image.open(f'img/{planets[current_id]}.png')
    # paint background
    image.paste(background_image, (0, 0))
    # put the planet in the foreground
    image.paste(planet_image, (-95, 0), planet_image)
    
    # place texts
    time_scaled = get_current_planet_time_scaled(current_id)
    draw.text((75, 40), f'{time_scaled[0]}:{time_scaled[1]}:{time_scaled[2]}', font=Sans_bold, fill=Planet_Text_Colors[planets[current_id]])
    draw.text((75, 75), planets[current_id], font=Sans, fill=Planet_Text_Colors[planets[current_id]])
    
    
    
    disp.image(image, rotation)
    
    sleep(0.2)
    
    
    
    




