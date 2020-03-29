#!/usr/bin/python3
import time
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

# quick test to see whether the buttons work properly

mode_button = 29
up_button = 31
down_button = 33

def button1_callback(channel):
    global start
    global end
    if GPIO.input(mode_button) == 1:
        start = time.time()
        print('Setting start time')
    if GPIO.input(mode_button) == 0:
        end = time.time()
        elapsed = end - start
        print('Button 1 was pushed for ' + str(elapsed) + 's')

def button2_callback(channel):
    print("Button 2 was pushed!")

def button3_callback(channel):
    print("Button 3 was pushed!")

GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(mode_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(up_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(down_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(mode_button, GPIO.BOTH, callback=button1_callback, bouncetime=200)
GPIO.add_event_detect(up_button, GPIO.RISING, callback=button2_callback, bouncetime=200)
GPIO.add_event_detect(down_button, GPIO.RISING, callback=button3_callback, bouncetime=200)

MESSAGE = input("Press enter to quit\n\n") # Run until someone presses enter
GPIO.cleanup() # Clean up
