import time
from datetime import datetime, timedelta
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import qwiic_keypad
import sys

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
image = Image.new("RGB", (width, height))
rotation = 90
draw = ImageDraw.Draw(image)

padding = -2
top = padding
bottom = height - padding

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("font/RetroGaming.ttf", 30)



# these setup the code for our buttons and the backlight and tell the pi to treat the GPIO pins as digitalIO vs analogIO
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

x = 0
y = 0
keyinput = ""
font_color = "#FFFFFF"  

while True:
    draw.rectangle((0, 0, width, height), outline=0, fill=000)
    myKeypad.update_fifo()  
    button = myKeypad.get_button()
    charButton = chr(button)
    if button != 0:
        if charButton == '#':
            keyinput += '#'
        elif charButton == '*':
            keyinput += ' '
        else: 
            # print(charButton, end="")
            keyinput += charButton
            print(keyinput)
    draw.text((x, y), keyinput, font=font, fill=font_color)
        
    # Flush the stdout buffer to give immediate user feedback
    sys.stdout.flush()
          
    # Display image.
    disp.image(image, rotation)
    time.sleep(.25)