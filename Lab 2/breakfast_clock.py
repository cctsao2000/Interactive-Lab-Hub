import time
from datetime import datetime, timedelta
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import qwiic_keypad
import sys
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

myKeypad = qwiic_keypad.QwiicKeypad()
myKeypad.begin()
button = 0

# Create blank image for drawing.

# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
# image = Image.new("RGB", (width, height))
rotation = 90
image = Image.new("RGB", (width, height))
rotation = 90
draw = ImageDraw.Draw(image)

padding = -2
top = padding
bottom = height - padding

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("font/TahitiSansD.otf", 35)
time_font = ImageFont.truetype("font/LemonDays.ttf", 50)


# these setup the code for our buttons and the backlight and tell the pi to treat the GPIO pins as digitalIO vs analogIO
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

x = 0
y = top
keyinput = "0840"
displaytxt = ""
font_color = "#FFFFFF"  
mode = 0
breakfast_option = {30:['Egg and Bacon', 'Pancake'], 20:['Egg'],10:['Yogurt','Bread', 'Cereal and Milk'], 5:['Banana', 'Milk', 'Cheese']}
result = ""

def checktime(timestr: str) -> bool:
    hourinput = int(timestr[0:2])
    mininput = int(timestr[2:4])
    if not hourinput < 24 or not mininput < 60:
        return False
    else:
        return True

def breakfastchoice(remain_min):
    if remain_min < 5:
        choice = "Just GO!"
    elif remain_min < 10:
        choice = random.choice(breakfast_option[5])
    elif remain_min < 20:
        choice = random.choice(breakfast_option[10])
    elif remain_min < 30:
        choice = random.choice(breakfast_option[20])
    else:
        choice = random.choice(breakfast_option[30])
    return choice

while True:
    if mode == 0: # main menu
        draw.rectangle((0, 0, width, height), outline=0, fill=000)
        draw.text((x+30, y+10), "Breakfast Clock", font=font, fill="#D9DCD6")        
        now_time = time.strftime("%H:%M")
        draw.text((x+65, y+50), now_time, font=time_font, fill="#F3BA20")
    elif mode == 1: # recommend breakfast option
        draw.rectangle((0, 0, width, height), outline=0, fill=000)
        record_hour = int(keyinput[0:2])
        record_min = int(keyinput[2:4])
        now_hour = int(now_time[0:2])
        now_min = int(now_time[3:5])
        remain_min = (((record_hour - now_hour) * 60 + record_min) - now_min)
        if now_hour > record_hour:
            btr = "See You Nextday"
        else:
            btr = "BTR {:2d} min".format(remain_min)
        draw.text((x+30, y+10), btr, font=font, fill=font_color)
        draw.text((x+30, y+50), result, font=font, fill=font_color)
        # draw.text((x+65, y+50), displaytxt, font=time_font, fill=font_color)
    else: # set when2breakfast
        draw.rectangle((0, 0, width, height), outline=0, fill=000)
        myKeypad.update_fifo()  
        button = myKeypad.get_button()
        charButton = chr(button)
        keyinput = keyinput[-4:]
        if button != 0:
            if charButton == '#':
                if checktime(keyinput):
                    displaytxt = "{:02d}:{:02d}".format(int(keyinput[0:2]), int(keyinput[2:4]))
                else:
                    keyinput = '0000'
                    displaytxt = 'invalid'
            elif charButton == '*':
                keyinput = keyinput[:-1]
            else: 
                keyinput += charButton
        else:
            displaytxt = "{:02d}:{:02d}".format(int(keyinput[0:2]), int(keyinput[2:4]))
        draw.text((x+60, y+10), "When to Go", font=font, fill=font_color)
        draw.text((x+65, y+50), displaytxt, font=time_font, fill=font_color)
        # Flush the stdout buffer to give immediate user feedback
        sys.stdout.flush()
    if buttonB.value and not buttonA.value:  # just button A pressed -> What to Eat
        if mode == 1:
            result = breakfastchoice(remain_min)
            mode = 1 # -> Switch options
        else:
            mode = 1
    if buttonA.value and not buttonB.value:  # just button B pressed -> Set Time
        mode = 2
    if not buttonA.value and not buttonB.value:  # both pressed -> Home Page
        mode = 0
    # Display image.
    disp.image(image, rotation)
    # time.sleep(.25)