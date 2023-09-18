from __future__ import print_function
import pygame
import random
import math
import pygame
import board
import busio
import time
from PIL import Image
from adafruit_rgb_display.rgb import color565
import adafruit_rgb_display.st7789 as st7789
import time
import subprocess
import digitalio
import board
from time import strftime, sleep
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import random
import qwiic_joystick
import time
import sys
font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

myJoystick = qwiic_joystick.QwiicJoystick()
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None
myJoystick.begin()
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

height = disp.height  
width = disp.width


# Do the Installation
pygame.init()
showw = False
screen = pygame.display.set_mode([width,height])

# Change the Title
pygame.display.set_caption("Car Game")

# Change the Logo
icon = pygame.image.load("logo.png")
icon = pygame.transform.scale(icon, (35,35))
pygame.display.set_icon(icon)

# Set the Player
def player(x,y):
    img_player = pygame.image.load("car.png")
    img_player = pygame.transform.scale(img_player, (35,35))
    screen.blit(img_player, (x,y))
    
x_player = 0
y_player =height-40
x_player_point = 0

# Set the Enemy
def enemy(x,y):
    img_enemy = pygame.image.load("enemy.png")
    screen.blit(img_enemy,(x,y))

x_enemy = random.randint(10,100)
y_enemy = random.randint(25,30)
y_enemy_point = 6

# Make the Collision Detection
def collision(x_player,y_player,x_enemy,y_enemy):
    distance = math.sqrt(math.pow(x_player-x_enemy,2)) + (math.pow(y_player-y_enemy,2))
    if distance < 30:
        return True
    else:
        return False

# Set the Score
score = 0
font = pygame.font.Font('freesansbold.ttf', 16)

def show_score(x,y):
    score_number = font.render("score:" + str(score), True, (255,255,255))
    screen.blit(score_number,(x,y))

x_score = 10
y_score = 10
    
# Frame Border
clock = pygame.time.Clock()

# Running the Game
running = True
starttime = time.time()
while running:
    # Change the Screen Color
    screen.fill((0,0,0))
    # Input the Loop
    x = myJoystick.horizontal
    y = myJoystick.vertical
    b = myJoystick.button

    if x > 575:
        x_player_point -= 0.4
    elif x < 450:
        x_player_point += 0.4
    
    # Set the Player Movement
    x_player += x_player_point
    if x_player >= 135:
        x_player = -10
    if x_player <= -30:
        x_player = 135

    #Set the Enemy Movement
    y_enemy += y_enemy_point
    if y_enemy >= 240:
        x_enemy = random.randint(-5,120)
        y_enemy = random.randint(5,10)
        score += 1
    
    # Show the Collision
    tabrakan = collision(x_player,y_player,x_enemy,y_enemy)
    if tabrakan:
        f = True
        while f == True:
            draw = ImageDraw.Draw(image)
            draw.rectangle((0, 0, width, height), outline=0,fill=(0,0,0))
            draw.text((0,0),"CONGRATS! \n\nYou've just \n\nWasted: \n\n\n" + str(int(elapsedTime)) + " Seconds", end="", font=font2, fill="#FFFFFF")
            disp.image(image)
            starttime = time.time()
            if myJoystick.button==0:
                score = 0
                f = False
                x_player = 0
                y_player =height-40
                x_player_point = 0
                x_enemy = random.randint(10,100)
                y_enemy = random.randint(25,30)
                y_enemy_point = 6

                 
    #Time
    clock.tick(60)

    # Show the Player
    player(x_player, y_player)

    # Show the Enemy
    enemy(x_enemy, y_enemy)

    # Show the Score
    if not buttonA.value:
        showw = True
    if not buttonB.value:
        showw = False
        
    if showw == True:
        show_score(x_score,y_score)

    pygame.display.update()
    image = Image.frombytes("RGB", (width, height), pygame.image.tostring(screen, "RGB"))
    disp.image(image)
    stoptime = time.time()
    elapsedTime = stoptime-starttime

pygame.quit()

