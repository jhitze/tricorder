import time
import board
import neopixel
import touchio
import digitalio
import asyncio
from pages import RED, YELLOW, GREEN, BLACK
from pages.temperature import TemperaturePage
from pages.co2 import Co2Page


i2c = board.I2C()
display = board.DISPLAY
pixel_pin = board.NEOPIXEL
num_pixels = 4

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=False)

# Perform a couple extra steps for the HalloWing M4
try:
    if getattr(board, "CAP_PIN"):
        # Create digitalio objects and pull low for HalloWing M4
        cap_pin = digitalio.DigitalInOut(board.CAP_PIN)
        cap_pin.direction = digitalio.Direction.OUTPUT
        cap_pin.value = False
except AttributeError:
    pass

touch_A2 = touchio.TouchIn(board.TOUCH1)
touch_A3 = touchio.TouchIn(board.TOUCH2)
touch_A4 = touchio.TouchIn(board.TOUCH3)
touch_A5 = touchio.TouchIn(board.TOUCH4)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)


max_co2 = 0

# Do something to show that it's loading.
rainbow_cycle(0)



class Pages():
    def __init__(self, display_width, i2c, pixels):
        self.display_width = display_width
        self.i2c = i2c
        self.pixels = pixels
        self.co2_page = Co2Page(display.width, i2c, pixels)
        self.temperature_page = TemperaturePage(display.width)
        self.current_page = self.co2_page
        self.__update_display__()
    
    def show_co2_page(self):
        self.current_page = self.co2_page
        self.__update_display__()
    
    def show_temperature_page(self):
        self.current_page = self.temperature_page
        self.__update_display__()
    
    def __update_display__(self):
        board.DISPLAY.show(self.current_page.group)
    

color_chase(BLACK, 0.01)

async def user_input_checker(pages):
    while True:
        if touch_A2.value:
            print("a2 was touched")
            pages.show_co2_page()
        elif touch_A3.value:
            print("a3 was touched")
            pages.show_temperature_page()
        await asyncio.sleep(0)

async def refresh_page(pages):
    while True:
        print(pages.current_page)
        await pages.current_page.check_sensor_readiness()
        pages.current_page.update_values()
        await asyncio.sleep(0)

async def main():
    pages = Pages(display.width, i2c, pixels)
    while True:
        user_input_task = asyncio.create_task(user_input_checker(pages))
        page_update_task = asyncio.create_task(refresh_page(pages))
        
        # This will run forever, because user input task never exits.
        await asyncio.gather(user_input_task, page_update_task)
        

asyncio.run(main())
