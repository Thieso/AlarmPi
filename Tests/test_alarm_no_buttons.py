#!/usr/bin/python
import time
import pygame
from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport
from luma.core.render import canvas
from luma.led_matrix.device import max7219
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, LCD_FONT, TINY_FONT

# defines the state the program is in, 0 for showing the clock, 1 for changing
# hours, 2 for changing minutes and 3 for beeping
STATE = 0
# set hours and minutes for the alarm
HOURS = 6
MINUTES = 30


# main function
def main():
    # wait some time to let the pi start up correctly
    #time.sleep(20)

    # define serial and device in order to interact with the LED matrix
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=4, block_orientation=0, rotate=2)
    virtual = viewport(device, width=32, height=8)

    # set initial contrast of the disyplay 
    device.contrast(20)

    # set blink time
    blinkTime = 0.5

    # initialize hour and time string
    timeString = 0
    hour = 0

    global STATE, HOURS, MINUTES
    while True:
        time.sleep(blinkTime)
        # set time string
        newTimeString = time.strftime('%H%M')

        # set alarm string for the right time
        hourString = str(HOURS).zfill(2)
        minuteString = str(MINUTES).zfill(2)
        alarmString = hourString + minuteString
        alarmString = alarmString

        # set contrast based on time
        # newHour = int(time.strftime('%H'))
        # if hour != newHour:
            # hour = newHour
            # contrast = getContrast(hour)
            # device.contrast(contrast)

        # if timeString == alarmString and STATE != 3:
            # STATE = 3
            # print("Sounding Alarm")
            # displayText(virtual, alarmString)
            # # blink all the numbers during alarm sounding
            # # in order to not ring again wait till minute passed
            # while time.strftime('%H%M') == alarmString:
                # time.sleep(1)

        # display information depeing on the state
        if STATE == 0:
            timeString = newTimeString
            # display time on display
            displayText(virtual, timeString)
        elif STATE == 1:
            # blink the hours on the display
            displayText(virtual, alarmString)
            time.sleep(blinkTime)
            alarmString = "--" + str(MINUTES).zfill(2)
            displayText(virtual, alarmString)
        elif STATE == 2:
            # blink the minutes on the display
            displayText(virtual, alarmString)
            time.sleep(blinkTime)
            alarmString = str(HOURS).zfill(2) + "--"
            displayText(virtual, alarmString)

# display text string on the display
def displayText(virtual, displayText):
    with canvas(virtual) as draw:
        text(draw, (1, 0), displayText, fill="white")

# get contrast based on hour of the day 
def getContrast(hours):
    b = 4.58e-3
    c = -2.19e-1
    d = 2.63
    f = 5
    contrast = b*pow(hours,4) + c*pow(hours,3) + d*pow(hours,2) + f
    return min(int(contrast), 100)

if __name__ == '__main__':
    try:
        main()
    finally:
        print('Cleaning up')
        GPIO.cleanup()
