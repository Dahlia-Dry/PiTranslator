import digitalio
import busio
import board
from adafruit_epd.epd import Adafruit_EPD
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
ecs = digitalio.DigitalInOut(board.D5)
dc = digitalio.DigitalInOut(board.D22)
rst = digitalio.DigitalInOut(board.D27)
busy = digitalio.DigitalInOut(board.D4)
srcs = None

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(6, GPIO.OUT)
from adafruit_epd.il0373 import Adafruit_IL0373
display = Adafruit_IL0373(104,212, spi, cs_pin=ecs, dc_pin=dc, sramcs_pin=srcs,
                          rst_pin=rst, busy_pin=busy)
#for flexible display:
display.set_black_buffer(1, False)
display.set_color_buffer(1, False)

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

display.rotation = 1

def pil_example():
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
	text = "Hello World!"
	(font_width, font_height) = font.getsize(text)
	draw.text(
    	(display.width // 2 - font_width // 2, display.height // 2 - font_height // 2),
    	text,
    	font=font,
    	fill=TEXT_COLOR,
	)

	# Display image.
	print('displaying image:')
	GPIO.output(6,GPIO.HIGH)
	display.image(image)
	display.display()

def mono_test():
	display.fill(Adafruit_EPD.WHITE)
	display.fill_rect(0, 0, 50, 60, Adafruit_EPD.BLACK)
	display.hline(80, 30, 60, Adafruit_EPD.BLACK)
	display.vline(80, 30, 60, Adafruit_EPD.BLACK)
	print('displaying image:')
	GPIO.output(6,GPIO.HIGH)
	display.display()

pil_example()
