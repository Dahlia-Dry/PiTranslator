from pynput import keyboard
import digitalio
import busio
import board
from adafruit_epd.epd import Adafruit_EPD
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO
from adafruit_epd.il0373 import Adafruit_IL0373
import time

#EINK 1---------------------------------------------------------------------
spi1 = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
ecs1 = digitalio.DigitalInOut(board.D5)
dc1 = digitalio.DigitalInOut(board.D22)
rst1 = digitalio.DigitalInOut(board.D27)
busy1 = digitalio.DigitalInOut(board.D4)
srcs1 = None

display1 = Adafruit_IL0373(104,212, spi1, cs_pin=ecs1, dc_pin=dc1, sramcs_pin=srcs1,
                          rst_pin=rst1, busy_pin=busy1)
#for flexible display:
display1.set_black_buffer(1, False)
display1.set_color_buffer(1, False)
#---------------------------------------------------------------------------

#EINK 2 --------------------------------------------------------------------
spi2 = busio.SPI(board.SCK_1, MOSI=board.MOSI_1, MISO=board.MISO_1)
ecs2 = digitalio.DigitalInOut(board.D26)
dc2 = digitalio.DigitalInOut(board.D13)
rst2 = digitalio.DigitalInOut(board.D23)
busy2 = digitalio.DigitalInOut(board.D24)
srcs2 = None
display2 = Adafruit_IL0373(104,212, spi2, cs_pin=ecs2, dc_pin=dc2, sramcs_pin=srcs2,
                          rst_pin=rst2, busy_pin=busy2)
#for flexible display:
display2.set_black_buffer(1, False)
display2.set_color_buffer(1, False)
#----------------------------------------------------------------------------
# First define some color constants
WHITE = (0xFF, 0xFF, 0xFF)
BLACK = (0x00, 0x00, 0x00)
RED = (0xFF, 0x00, 0x00)
 # Next define some constants to allow easy resizing of shapes and colors
BORDER = 20
FONTSIZE = 24
BACKGROUND_COLOR = BLACK
FOREGROUND_COLOR = WHITE
TEXT_COLOR = BLACK

cursor = 0

def drawletter(display, letter, c):
	display.rotation = 1
	image = Image.new("RGB", (display.width, display.height))

	# Get drawing object to draw on image.
	draw = ImageDraw.Draw(image)
	if c == 0:
		draw.rectangle((0, 0, display.width, display.height),
			 fill=FOREGROUND_COLOR)

	# Load a TTF Font
	font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONTSIZE)

	# Draw Some Text
	text = letter
	(font_width, font_height) = font.getsize(text)
	draw.text(
    	(c, 0),
    	text,
    	font=font,
    	fill=TEXT_COLOR,
	)
	# Display image.
	print('displaying text:')
	display.image(image)
	display.display()
	print(font_width)
	return font_width

def on_press(key):
    global cursor
    try:
        width = drawletter(display1, key.char, cursor)
        print(width)
        cursor += width
        print('wrote ',key.char)
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False

def main():
    listener= keyboard.Listener(on_press = on_press,
                                on_release = on_release)
    listener.start()
    while True:
       print('ass')
main()
