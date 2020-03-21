import time
from luma.core.virtual import viewport
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.led_matrix.device import max7219
from luma.core.legacy import text
from luma.core.legacy.font import proportional, LCD_FONT

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=4, block_orientation=0)
device.contrast(10)


virtual = viewport(device, width=32, height=8)

i = 0
while True:
    i = i + 1
    with canvas(virtual) as draw:
        text(draw, (1, 0), str(i), fill="white")
        time.sleep(0.1)
    print(str(i))
