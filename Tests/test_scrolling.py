#!/usr/bin/python3
import time
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport
from luma.core.render import canvas
from luma.led_matrix.device import max7219
from luma.core.legacy import text, show_message

# script to test if scrolling works for the display of the date

# setup device
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=4, block_orientation=-90, rotate=1)
virtual = viewport(device, width=8, height=len(text_string) * 8)

# define the string that is scrolling over the display
text_string = "scrolling"

# scroll the text indefinetly
while True:
    # show_message(device, text_string, fill="white", scroll_delay=0.1)
    with canvas(virtual) as draw:
        for i, word in enumerate(text_string):
            text(draw, (0, i*8), word, fill="white")
    time.sleep(1)

    for offset in range(virtual.height - device.height):
        virtual.set_position((0, offset))
        time.sleep(0.1)
