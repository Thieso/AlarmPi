#!/usr/bin/python3
import time
from luma.core.virtual import viewport
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219
from luma.core.legacy import text
from luma.core.legacy.font import proportional, LCD_FONT

# test whether the LED matrix displays anything to see whether it works
# correctly

# setup device
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=4, block_orientation=-90, rotate=1)
virtual = viewport(device, width=8, height=32)
device.contrast(100)

# display increasing numbers
i = 0
while True:
    i = i + 1
    with canvas(virtual) as draw:
        for i, word in enumerate(str(i)):
            text(draw, (1, i*8), word, fill="white")
        time.sleep(0.1)
    print(str(i))
