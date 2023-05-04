# PiicoDev SSD1306 demo code
# Show off some features of the PiicoDev OLED driver
#
# This example code is adapted from https://raw.githubusercontent.com/CoreElectronics/CE-PiicoDev-SSD1306-MicroPython-Module/main/main.py
# to work with the simplied library
#
# NOTE: This adapted example has only been tested on the Raspberry Pi Pico

import math
from machine import Pin, I2C
from utime import sleep_ms
from ssd1306 import SSD1306_I2C

WIDTH  = 128                                            # oled display width
HEIGHT = 64                                             # oled display height
i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=200000)       # Init I2C using pins GP8 & GP9 (default I2C0 pins)
print("I2C Address      : "+hex(i2c.scan()[0]).upper()) # Display device address
print("I2C Configuration: "+str(i2c))                   # Display I2C config

class graph2D:
    def __init__(self, originX = 0, originY = HEIGHT-1, width = WIDTH, height = HEIGHT, minValue=0, maxValue=255, c = 1, bars = False):
        self.minValue = minValue
        self.maxValue = maxValue
        self.originX = originX
        self.originY = originY
        self.width = width
        self.height = height
        self.c = c
        self.m = (1-height)/(maxValue-minValue)
        self.offset = originY-self.m*minValue
        self.bars = bars
        self.data = []

def updateGraph2D(display: SSD1306_I2C, graph, value):
    graph.data.insert(0,value)
    if len(graph.data) > graph.width:
        graph.data.pop()
    x = graph.originX+graph.width-1
    m = graph.c
    for value in graph.data:
        y = round(graph.m*value + graph.offset)
        if graph.bars == True:
            for idx in range(y, graph.originY+1):
                if x >= graph.originX and x < graph.originX+graph.width and idx <= graph.originY and idx > graph.originY-graph.height:
                    display.pixel(x,idx, m)
        else:
            if x >= graph.originX and x < graph.originX+graph.width and y <= graph.originY and y > graph.originY-graph.height:
                display.pixel(x,y, m)
        x -= 1

display = SSD1306_I2C(WIDTH, HEIGHT, i2c)                  # Init oled display

# Text and numbers
for counter in range(0,101):
    display.fill(0)
    display.text("PiicoDev",30,20, 1)
    display.text(str(counter),50,35, 1)
    display.show()
sleep_ms(500)

# Bargraphs
thick = 15 # thickness of the bar
for val in range(WIDTH+1):
    display.fill(0)
    display.text("Bargraphs", 20, 10, 1)
    display.fill_rect(0, HEIGHT-thick, val, thick, 1) # Filled bar graph
    display.rect(0, int(HEIGHT-2*thick - 5), int(val/2), thick, 1) # no-fill
    display.show()
sleep_ms(500)

# Plots
graphSin = graph2D()
graphCos = graph2D()
for x in range(128):
    s = int(math.sin(x/10.0)*HEIGHT+HEIGHT+30)
    c = int(math.cos(x/10.0)*HEIGHT+HEIGHT+30)
    display.fill(0)
    display.text("Plots", 50, 10, 1)
    updateGraph2D(display, graphSin,s)
    updateGraph2D(display, graphCos,c)
    display.show()
sleep_ms(1000)

# Bouncy Square animation
square = 15   # square edge length (px)
x = (WIDTH-1)/2   # starting position
y = (HEIGHT-1)/2  # starting y position

v = {
    'x': 2.3, # Starting velocity (pixels per animation frame)
    'y': 3.5
}

collisionCount = 0
while True:
    display.fill(0) # empty the frame buffer
    
    # Next position = Current Position + Velocity
    x = x + v['x']
    y = y + v['y']
    
    # Check for boundary collision
    if x > WIDTH-square or x < 0:
        v['x']=-v['x'] # reverse the x-velocity
        collisionCount = collisionCount + 1
    if y >= HEIGHT-square or y < 0:
        v['y']=-v['y'] # reverse the x-velocity
        collisionCount = collisionCount + 1
    
    # draw the rectangle
    display.fill_rect(round(x), round(y), square, square, 1)
    
    # draw boundaries
    display.hline(0,0,WIDTH,1)
    display.vline(0,0,HEIGHT,1)
    display.vline(WIDTH-1,0,HEIGHT, 1)
    display.hline(0,HEIGHT-1,WIDTH, 1)
    
    # show the collision count
    display.text(str(collisionCount),10,round(HEIGHT/2), 1)
    display.show()
    sleep_ms(10)
