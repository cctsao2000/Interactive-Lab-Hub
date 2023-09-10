import time
from datetime import datetime, timedelta
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

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
draw = ImageDraw.Draw(image)

padding = -2
top = padding
bottom = height - padding

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("font/RetroGaming.ttf", 30)
font1 = ImageFont.truetype("font/stickman.ttf", 90)
font2 = ImageFont.truetype("font/stickman.ttf", 30)


# these setup the code for our buttons and the backlight and tell the pi to treat the GPIO pins as digitalIO vs analogIO
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

x = -10
xs = 40
ys = top + 15
mode = 0
x_study = 85
y_study = 80
study = ""
min_count = -1
tomato_count = 0
xt = 0 
yt = 0
kick = 0
direction = 1

while True:
    draw.rectangle((0, 0, width, height), outline=0, fill=000)
    now_time = time.strftime("%H:%M:%S")
    now_hour = int(now_time[0:2])
    now_min = int(now_time[3:5])
    now_sec = int(now_time[-2:])
    y = bottom - 70
    
    if mode == 0: #normal
        xs = 40
        study = ""
        if now_hour >= 23 or now_hour <= 6:
            action = "h"
        else:
            if now_sec % 2 == 1:
                action = "k"
            else:
                y -= 5
                action = "l"  
            x += 2
        if x > 230:
            x = -10 
        draw.text((xs, ys), now_time, font=font, fill='white')
    
    elif mode == 1: #study
        total = ((((now_hour - record_hour) * 60 + now_min) - record_min) * 60 + now_sec) - record_sec
        remain_sec = 10 - total
        xs = 100
        now_time = "{:02d}:{:02d}".format(divmod(remain_sec, 60)[0],divmod(remain_sec, 60)[1])
        study = "STUDY!"
        if remain_sec == 0:
            tomato_count += 1
            record_hour = now_hour
            record_min = now_min
            record_sec = now_sec
        draw.polygon([(25,12), (27, 20), (23,20)], fill=(0,255,0))
        draw.polygon([(15,15), (27, 20), (23,20)], fill=(0,255,0))
        draw.polygon([(35,15), (27, 20), (23,20)], fill=(0,255,0))
        draw.ellipse((15, 18, 40, 35), outline=0, fill=400)
        draw.text((45, 10), str(tomato_count), font=font2, fill='white')
        action = "–"   
        
    else: #game
        draw.polygon([(25,12), (27, 20), (23,20)], fill=(0,255,0))
        draw.polygon([(15,15), (27, 20), (23,20)], fill=(0,255,0))
        draw.polygon([(35,15), (27, 20), (23,20)], fill=(0,255,0))
        draw.ellipse((15, 18, 40, 35), outline=0, fill=400)
        draw.text((45, 10), str(tomato_count), font=font2, fill='white')
        action = "k"   
        study = ""
        now_time = ""
        draw.rectangle((220, 5+yt, 230, 30+yt), outline=0, fill='white')
        yt += 10 * direction
        if yt > 100:
            direction = -1
        if yt < 0:
            direction = 1
        if tomato_count > 0:
            if kick == 1:
                while xt < 180:
                    xt += 10
            draw.polygon([(47+xt,102), (49+xt, 110), (45+xt,110)], fill=(0,255,0))
            draw.polygon([(37+xt,105), (49+xt, 110), (45+xt,110)], fill=(0,255,0))
            draw.polygon([(57+xt,105), (49+xt, 110), (45+xt,110)], fill=(0,255,0))
            draw.ellipse((35+xt, 108, 60+xt, 125), outline=0, fill=400)
            xt = 0
            kick = 0
                
        
        
    # Draw a black filled box to clear the image. (should be red if fill=400)
    # now_time = time.strftime("%m/%d/%Y %H:%M:%S")
    font_color = "#FFFFFF"
    
    if buttonB.value and not buttonA.value:  # just button A pressed -> Study Mode
        if mode == 1:
            mode = 1
        else:
            record_hour = now_hour
            record_min = now_min
            record_sec = now_sec
            mode = 1
    if buttonA.value and not buttonB.value:  # just button B pressed -> Game Mode
        if mode == 2:
            if tomato_count > 0:
                tomato_count -= 1
                action = "n"
                kick = 1
        else:
            mode = 2
            record_sec = now_sec
    if not buttonA.value and not buttonB.value:  # both pressed
        mode = 0
                
    draw.text((xs, ys), now_time, font=font, fill=font_color)
    draw.text((x, y), action, font=font1, fill=font_color)
    draw.text((x_study, y_study), study, font=font, fill=font_color)
    
    # Display image.
    disp.image(image, rotation)