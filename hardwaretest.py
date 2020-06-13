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
#LEDs------------------------------------------------------------------------
green = digitalio.DigitalInOut(board.D6)
green.direction = digitalio.Direction.OUTPUT
red = digitalio.DigitalInOut(board.D12)
red.direction = digitalio.Direction.OUTPUT
yellow1 = digitalio.DigitalInOut(board.D19)
yellow1.direction = digitalio.Direction.OUTPUT
yellow2 = digitalio.DigitalInOut(board.D16)
yellow2.direction = digitalio.Direction.OUTPUT
blue1 = digitalio.DigitalInOut(board.D18)
blue1.direction = digitalio.Direction.OUTPUT
blue2 = digitalio.DigitalInOut(board.D17)
blue2.direction = digitalio.Direction.OUTPUT
white1 = digitalio.DigitalInOut(board.D25)
white1.direction = digitalio.Direction.OUTPUT
white2 = digitalio.DigitalInOut(board.CE1)
white2.direction = digitalio.Direction.OUTPUT

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


def pil_example(display):
	display.rotation = 1
	image = Image.new("RGB", (display.width, display.height))

	# Get drawing object to draw on image.
	draw = ImageDraw.Draw(image)

	# Draw a filled box as the background
	draw.rectangle((0, 0, display.width, display.height), fill=BACKGROUND_COLOR)

	# Draw a smaller inner foreground rectangle
	draw.rectangle(
    	(BORDER, BORDER, display.width - BORDER - 1, display.height - BORDER - 1),
    	fill=FOREGROUND_COLOR,
	)

	# Load a TTF Font
	font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONTSIZE)

	# Draw Some Text
	text = "i still work!"
	(font_width, font_height) = font.getsize(text)
	draw.text(
    	(display.width // 2 - font_width // 2, display.height // 2 - font_height // 2),
    	text,
    	font=font,
    	fill=TEXT_COLOR,
	)

	# Display image.
	print('displaying image:')
	display.image(image)
	display.display()

def mono_test(display):
	display.fill(Adafruit_EPD.WHITE)
	display.fill_rect(0, 0, 50, 60, Adafruit_EPD.BLACK)
	display.hline(80, 30, 60, Adafruit_EPD.BLACK)
	display.vline(80, 30, 60, Adafruit_EPD.BLACK)
	print('displaying image:')
	display.display()

def blink_test():
    while True:
        green.value = True
        red.value = True
        yellow1.value = True
        yellow2.value = True
        blue1.value = True
        white1.value = True
        blue2.value = True
        white2.value = True
        time.sleep(0.5)
        green.value = False
        red.value = False
        yellow1.value = False
        yellow2.value = False
        blue1.value = False
        white1.value = False
        blue2.value = False
        white2.value = False


pil_example(display1)
pil_example(display2)
blink_test()
