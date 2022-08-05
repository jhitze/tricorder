import time
import board
import neopixel
import touchio
import digitalio
import adafruit_scd30
from pages import YELLOW, GREEN, BLACK
from pages.temperature import TemperaturePage
from pages.co2 import Co2Page


i2c = board.I2C()
scd30 = adafruit_scd30.SCD30(i2c)
scd30.measurement_interval = 5
display = board.DISPLAY

color = 0x11bf08

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

co2_page = Co2Page(display.width)
temperature_page = TemperaturePage(display.width)

board.DISPLAY.show(co2_page.group)

page = 0

while True:
    if page == 0:
        color_chase(YELLOW, 0.01)
        while scd30.data_available != 1:
                time.sleep(0.200)

        try:
            co2 = scd30.CO2
            temp = scd30.temperature
            relh = scd30.relative_humidity
            color_chase(GREEN, 0.01)
            color_chase(BLACK, 0.01)
        except Exception:
            pass
        co2_page.update_co2(co2)
        co2_page.update_temp_and_relh(temp, relh)

        print("Co2: " + str(co2))
        print("Temp: " + str(temp))
        print("Humidity: " + str(relh))

    elif page == 1:
        # c02_label.text = "page 2 top"
        # cognitive_function_label.text = "page 2 middle"
        # max_co2_label.text = "page 2 bottom"
        # temp_and_humidity_label.text = temp_and_humidity_text(temp, relh)
        pass

    elif page == 2:
        pass
        # c02_label.text = "page 3 top"
        # cognitive_function_label.text = "page 3 middle"
        # max_co2_label.text = "page 3 bottom"
        # temp_and_humidity_label.text = temp_and_humidity_text(temp, relh)

    for time_left in range(50,0,-1):
        
        if touch_A2.value:
            board.DISPLAY.show(co2_page.group)
            continue
        elif touch_A3.value:
            board.DISPLAY.show(temperature_page.group)
            continue

        co2_page.refresh_label.text = co2_page.refresh_text(time_left)

        time.sleep(0.01)
        