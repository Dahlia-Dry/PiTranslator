import digitalio
import busio
import board
from adafruit_epd.epd import Adafruit_EPD
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO
from adafruit_epd.il0373 import Adafruit_IL0373
import time
import xmltodict
import csv
import pandas as pd
import datetime
import textwrap
from pynput import keyboard

#SETUP:
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
FONTSIZE = 14
BACKGROUND_COLOR = WHITE
FOREGROUND_COLOR = WHITE
TEXT_COLOR = BLACK
# Load a TTF Font
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONTSIZE)
#load en-es dict
def parse(xml='es-en.xml'):
    #parse xml to dict with format dict['spanish word'] = (english definition, part of speech)
    with open(xml) as fd:
        doc = xmltodict.parse(fd.read())
    raw = doc['dic']['l']
    dict = {}
    for i in range(len(raw)):
        for j in range(len(raw[i]['w'])):
            dict[raw[i]['w'][j]['c']] = (raw[i]['w'][j]['d'],raw[i]['w'][j]['t'])
    return dict

dict = parse()
#End Setup----------------------------------------------------------------------
#Utility Functions-------------------------------------------------------------
def write_to_screen(display, text, x, y, clear=True):
    display.rotation = 1
    image = Image.new("RGB", (display.width, display.height))
    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)
    #clear screen
    if clear:
        draw.rectangle((0, 0, display.width, display.height), fill=BACKGROUND_COLOR)
	# Draw Some Text
    if type(text) is not list:
        text = [text]
        x = [x]
        y = [y]

    for i in range(len(text)):
        (font_width, font_height) = font.getsize(text[i])
        if len(text[i]) > 20:
            inc=0
            for wrap in textwrap.wrap(text[i],30):
                if inc == 0:
                    text[i] = wrap
                else:
                    text.insert(i+1, wrap)
                    x.insert(i+1, 0)
                    y.insert(i+1, y[i] + inc*font_height)
                inc +=1
    for i in range(len(text)):
        draw.text(
        	(x[i],y[i]),
        	text[i],
        	font=font,
        	fill=TEXT_COLOR,
    	)
    	# Display image.
    	#print('displaying text:')
    display.image(image)
    display.display()
    return font_width, font_height

def dictionary(query):
    #Write top screen as blank search
    font_width, font_height = write_to_screen(display1,'Search: ',0,0)
    #query = input()
    try:
        print('def:' + dict[query][0] + '\n' + dict[query][1])
        font_width, font_height = write_to_screen(display1, ['Search: '+query,'Add to Journal?'],[0,0],[0,font_height])
        font_width, font_height = write_to_screen(display2, [query + ':', dict[query][0]+','+dict[query][1]],[0,0],[0,font_height])
        add = input('Add to Journal?')
        if add == '':
            addtojournal(query)
            font_width, font_height = write_to_screen(display1, ['Search: '+query,'Add to Journal? Added.'],[0,0],[0,font_height])
    except KeyError:
        font_width, font_height = write_to_screen(display2,query + ' not found.',0,0)

def addtojournal(query):
    with open('journal.csv','a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([query,dict[query][0] + ',' + dict[query][1], '0',datetime.datetime.now()])

def sortjournal(mode):
    journal = pd.read_csv('journal.csv')
    if mode == 0: #old->new
        journal['created'] = pd.to_datetime(journal['created'])
        journal = journal.sort_values(by='created')
    elif mode == 1: #new->old
        journal['created'] = pd.to_datetime(journal['created'])
        journal = journal.sort_values(by='created',ascending=False)
    elif mode == 2: #low -> high score
        journal = journal.sort_values(by='score')
    elif mode == 3: #random
        journal = journal.sample(frac=1)
    else:
        raise TypeError('Invalid Mode; use 0,1,2, or 3')
    return journal

def newcard(index, mode):
    journal = sortjournal(mode)
    font_width, font_height = write_to_screen(display1,
                                            ['Term: ' + journal['definition'].iloc[index]],
                                            [0],[0])
    return journal

def checkcard(journal, index, query):
    if query == journal['word'].iloc[index]:
        journal['score'].iloc[index] = int(journal['score'].iloc[index])+1
        font_width, font_height = write_to_screen(display2,
                                                ['Guess: ' + query, 'Correct! :)'],
                                                [0,0],[0,font_height])
    else:
        journal['score'].iloc[index] = int(journal['score'].iloc[index])-1
        font_width, font_height = write_to_screen(display2,
                                                ['Guess: ' + query, 'Wrong :( Correct Word: ' + journal['word'].iloc[index]],
                                                [0,0],[0,font_height])
    journal.to_csv('journal.csv')

#end utility functions--------------------------------------------------------
def main():
    query = ""
    font_width, font_height = write_to_screen(display1,'Search:',0,0)
    while True:
        query = input()
        if query == '.':
            index = 0
            mode = 2
            while query != ',':
                journal = newcard(index, mode)
                query = input()
                if query == '0':
                    mode = 0
                    query = input()
                elif query == '1':
                    mode = 1
                    query = input()
                elif query == '2':
                    mode =2
                    query = input()
                elif query == '3':
                    mode=3
                    query = input()
                checkcard(journal, index, query)
                index +=1
        else:
            if query != ',':
                dictionary(query)
main()
