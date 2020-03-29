#!/usr/bin/python3
import pygame
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from Alarm import Alarm
from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport
from luma.core.render import canvas
from luma.led_matrix.device import max7219

# main function for the alarm clock 
def main():
    # define buttons for gpio input
    mode_button = 29
    up_button = 31
    down_button = 33

    # define serial and device in order to interact with the LED matrix
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=4, block_orientation=0, rotate=2)
    virtual = viewport(device, width=32, height=8)

    # create instance of Alarm
    alarm = Alarm(virtual, device)

    # setup buttons
    GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
    GPIO.setup(mode_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(up_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(down_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # bounce time for the buttons so that they work properly
    bounce_time = 200
    # setup callbacks for the buttons with pull down logic
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
