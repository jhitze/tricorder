import gc
import board
import neopixel
from pages.pages import Pages
import digitalio
import asyncio
import busio
from digitalio import DigitalInOut, Direction
from adafruit_seesaw import seesaw, rotaryio, digitalio


print( "After last load in Code.py Loaded Available memory: {} bytes".format(gc.mem_free()) )



# Perform a couple extra steps for the HalloWing M4
try:
    if getattr(board, "CAP_PIN"):
        # Create digitalio objects and pull low for HalloWing M4
        cap_pin = digitalio.DigitalInOut(board.CAP_PIN)
        cap_pin.direction = digitalio.Direction.OUTPUT
        cap_pin.value = False
except AttributeError:
    pass

i2c = busio.I2C(board.SCL, board.SDA, frequency=100000, timeout = 1000)
display = board.DISPLAY
pixel_pin = board.NEOPIXEL
button_pin = board.D10
num_pixels = 4
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=False)

next_button = DigitalInOut(button_pin)
next_button.direction = Direction.INPUT

seesaw = seesaw.Seesaw(i2c, 0x36)
seesaw.pin_mode(24, seesaw.INPUT_PULLUP)
button = digitalio.DigitalIO(seesaw, 24)


encoder = rotaryio.IncrementalEncoder(seesaw)

async def user_input_checker(pages):
    last_position = None
    button_held = False
    while True:
        position = encoder.position
        if position != last_position:
            last_position = position
            print("Position: {}".format(position))
            page_set_to = pages.goto_page(position)
            print("Page was set to: {}".format(page_set_to))
            encoder.position = page_set_to


        elif not button.value and not button_held:
            button_held = True
            print("Button pressed")
            

        elif button.value and button_held:
            button_held = False
            print("Button released")

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
