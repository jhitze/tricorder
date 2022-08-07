import gc
import board
import neopixel
from pages.pages import Pages
import touchio
import digitalio
import asyncio
from adafruit_debouncer import Debouncer


print( "After asyncio in Code Loaded Available memory: {} bytes".format(gc.mem_free()) )

i2c = board.I2C()
display = board.DISPLAY
pixel_pin = board.NEOPIXEL
num_pixels = 4
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=False)

print( "After board stuff done in Code Loaded Available memory: {} bytes".format(gc.mem_free()) )

# Perform a couple extra steps for the HalloWing M4
try:
    if getattr(board, "CAP_PIN"):
        # Create digitalio objects and pull low for HalloWing M4
        cap_pin = digitalio.DigitalInOut(board.CAP_PIN)
        cap_pin.direction = digitalio.Direction.OUTPUT
        cap_pin.value = False
except AttributeError:
    pass

touch_A2 = Debouncer(touchio.TouchIn(board.TOUCH1), interval=0.2)
touch_A3 = Debouncer(touchio.TouchIn(board.TOUCH2), interval=0.2)
touch_A4 = Debouncer(touchio.TouchIn(board.TOUCH3), interval=0.2)
touch_A5 = Debouncer(touchio.TouchIn(board.TOUCH4), interval=0.2)

async def user_input_checker(pages):
    while True:
        touch_A2.update()
        touch_A3.update()
        if touch_A2.value:
            print("a2 was touched")
            pages.previous()
        elif touch_A3.value:
            print("a3 was touched")
            pages.next()
        elif touch_A4.value:
            print("a4 was touched")
            # pages.show_voc_page()
        await asyncio.sleep(0)

async def refresh_page(pages):
    while True:
        await pages.current_page.run()
        await asyncio.sleep(0)

async def main():
    pages = Pages(i2c, pixels, board.DISPLAY)
    while True:
        user_input_task = asyncio.create_task(user_input_checker(pages))
        page_update_task = asyncio.create_task(refresh_page(pages))
        
        # This will run forever, because user input task never exits.
        await asyncio.gather(user_input_task, page_update_task)
        

asyncio.run(main())
