import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=None)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Alternatively load a different format image, resize it, and convert to 1 bit color.
image = Image.open('ALLAH.jpg').resize((disp.width, disp.height), Image.ANTIALIAS).convert('1')

# Display image.
disp.image(image)
disp.display()