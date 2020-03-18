#!/usr/bin/python
import time
import pygame
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from Alarm import Alarm
from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport
from luma.core.render import canvas
from luma.led_matrix.device import max7219
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, LCD_FONT, TINY_FONT

# main function
def main():
    # wait some time to let the pi start up correctly
    #time.sleep(20)

    # define buttons for gpio input
    mode_button = 29
    up_button = 37
    down_button = 15

    # define serial and device in order to interact with the LED matrix
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=4, block_orientation=0, rotate=2)
    virtual = viewport(device, width=32, height=8)

    # create instance of Alarm
    alarm = Alarm(virtual, device)

    # setup buttons
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    GPIO.setup(mode_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(up_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(down_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    bounce_time = 200
    # setup callbacks
    GPIO.add_event_detect(mode_button, GPIO.RISING, callback=alarm.state_callback, bouncetime=bounce_time)
    GPIO.add_event_detect(up_button, GPIO.RISING, callback=alarm.inc_callback, bouncetime=bounce_time)
    GPIO.add_event_detect(down_button, GPIO.RISING, callback=alarm.dec_callback, bouncetime=bounce_time)

    # start alarm loop
    alarm.alarm_loop()


if __name__ == '__main__':
    try:
        main()
    finally:
        print('Cleaning up')
        GPIO.cleanup()
