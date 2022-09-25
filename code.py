import gc
import board
from pages.pages import Pages
print( "After pages import Available memory: {} bytes".format(gc.mem_free()) )
import asyncio
from busio import I2C
from digitalio import DigitalInOut, Direction
from adafruit_seesaw import seesaw, rotaryio, digitalio

print( "After last load in Code.py Loaded Available memory: {} bytes".format(gc.mem_free()) )


# i2c = I2C(board.SCL, board.SDA, frequency=100000, timeout = 1000)
i2c = board.I2C()
display = board.DISPLAY
button_pin = board.D10
num_pixels = 4

option_button = DigitalInOut(button_pin)
option_button.direction = Direction.INPUT

seesaw = seesaw.Seesaw(i2c, 0x36)
seesaw.pin_mode(24, seesaw.INPUT_PULLUP)
button = digitalio.DigitalIO(seesaw, 24)


encoder = rotaryio.IncrementalEncoder(seesaw)

async def user_input_checker(pages):
    last_position = None
    button_held = False
    while True:
        try:
            position = encoder.position

            if position != last_position:
                last_position = position
                print("Position: {}".format(position))
                page_set_to = pages.goto_page(position)
                print("Page was set to: {}".format(page_set_to))
                encoder.position = page_set_to


            elif not button.value and not button_held:
                button_held = True
                print("Option button pressed")
                pages.option_clicked()


            elif button.value and button_held:
                button_held = False
                print("Button released")
        except Exception as ex:
            print("Error with encoder: {}".format(ex))
            board.I2C().unlock()

        await asyncio.sleep(0)

async def refresh_page(pages):
    while True:
        try:
            await pages.current_page.run()
        except Exception as ex:
            raise ex
        await asyncio.sleep(0)

async def main():
    print( "Main Started Available memory: {} bytes".format(gc.mem_free()) )
    pages = Pages(i2c, board.DISPLAY)
    user_input_task = asyncio.create_task(user_input_checker(pages))
    page_update_task = asyncio.create_task(refresh_page(pages))
    print( "After Tasks created Available memory: {} bytes".format(gc.mem_free()) )

    while True:
        # This will run forever, because user input task never exits.
        await asyncio.gather(user_input_task, page_update_task)
        

asyncio.run(main())
