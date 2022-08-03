import time
import board
import neopixel
import touchio
import digitalio
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes.rect import Rect
from analogio import AnalogIn
import adafruit_scd30

vbat_voltage = AnalogIn(board.VOLTAGE_MONITOR)


def get_voltage(pin):
    return (pin.value * 3.3) / 65536 * 2




i2c = board.I2C()
scd30 = adafruit_scd30.SCD30(i2c)



display = board.DISPLAY
# Set text, font, and color
font = bitmap_font.load_font("/font/Helvetica-Bold-16.bdf")
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

def c02_text(c02):
    return "CO2: {:.2f} PPM".format(c02)

# Numbers from Kurtis Baute
# https://www.youtube.com/watch?v=1Nh_vxpycEA
# https://www.youtube.com/watch?v=PoKvPkwP4mM
def cognitive_function_text(c02):
    if(c02 > 39000):
        return "Death Possible"
    elif(c02 >= 10000):
        return "Long Term Health Risk"
    elif(c02 >= 2000):
        return "Physical Problems Possible"
    elif(c02 >= 1400):
        return "50% Cognitive Decrease"
    elif(c02 >= 1000):
        return "15% Cognitive Decrease"
    elif(c02 > 500):
        return "Above outside levels"
    else:
        return "Outside level ~411ppm"

def max_co2_text(max_co2_level):
    return "Max CO2: {:.2f} PPM".format(max_co2_level)

def temp_and_humidity_text(temp, humidity):
    return "T: {:.2f}°C    H: {:.0f} %".format(temp, humidity)

def refresh_text(time_left):
    return "Refresh in {}".format(time_left)

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
BLACK = (0,0,0)

max_co2 = 0

### new display idea
BACKGROUND_COLOR = 0xFF0000
FOREGROUND_COLOR = 0xFFFFFF
BACKGROUND_TEXT_COLOR = 0xFFFFFF
FOREGROUND_TEXT_COLOR = 0x000000

# Do something to show that it's loading.
rainbow_cycle(0)

splash = displayio.Group()
board.DISPLAY.show(splash)
color_bitmap = displayio.Bitmap(240, 240, 1)
color_palette = displayio.Palette(1)
color_palette[0] = BACKGROUND_COLOR

bg_sprite = displayio.TileGrid(color_bitmap,
                               pixel_shader=color_palette,
                               x=0, y=0)
splash.append(bg_sprite)

# Draw a Foreground Rectangle where the name goes
rect = Rect(0, 50, 240, 140, fill=FOREGROUND_COLOR)
splash.append(rect)

# Setup and Center the header label
header_label = label.Label(font, text="Cheap-o Tricorder", color=color)
(x, y, w, h) = header_label.bounding_box
header_label.x = (120 - w // 2)
header_label.y = 20
header_label.color = BACKGROUND_TEXT_COLOR
splash.append(header_label)

# Setup and Center the c02 Label
c02_label = label.Label(font, text=c02_text(9999.99), line_spacing=1, max_glyphs=25)
(x, y, w, h) = c02_label.bounding_box
c02_label.x = (120 - w // 2)
c02_label.y = 60
c02_label.color = FOREGROUND_TEXT_COLOR
splash.append(c02_label)

# Setup and Center the health Label
cognitive_function_label = label.Label(font, text=cognitive_function_text(9999.99), line_spacing=1, max_glyphs=30)
(x, y, w, h) = cognitive_function_label.bounding_box
cognitive_function_label.x = (120 - w // 2)
cognitive_function_label.y = 90
cognitive_function_label.color = FOREGROUND_TEXT_COLOR
splash.append(cognitive_function_label)

# Setup and Center the health Label
max_co2_label = label.Label(font, text=max_co2_text(9999.99), line_spacing=1, max_glyphs=30)
(x, y, w, h) = max_co2_label.bounding_box
max_co2_label.x = (120 - w // 2)
max_co2_label.y = 120
max_co2_label.color = FOREGROUND_TEXT_COLOR
splash.append(max_co2_label)

# Setup and Center the temp and humidity Label
temp_and_humidity_label = label.Label(font, text=temp_and_humidity_text(99.99,99), line_spacing=1, max_glyphs=25)
(x, y, w, h) = temp_and_humidity_label.bounding_box
temp_and_humidity_label.x = (120 - w // 2)
temp_and_humidity_label.y = 180
temp_and_humidity_label.color = FOREGROUND_TEXT_COLOR
splash.append(temp_and_humidity_label)

# Setup and Center the refresh Label
refresh_label = label.Label(font, text=refresh_text(1), line_spacing=1, max_glyphs=15)
(x, y, w, h) = refresh_label.bounding_box
refresh_label.x = (120 - w // 2)
refresh_label.y = 220
refresh_label.color = FOREGROUND_TEXT_COLOR
splash.append(refresh_label)


scd30.measurement_interval = 5
page = 0

while True:
    if page == 0:
        color_chase(YELLOW, 0.01)
        while scd30.data_available != 1:
                time.sleep(0.200)
                #color_chase(YELLOW, 0.05)

        try:
            co2 = scd30.CO2
            temp = scd30.temperature
            relh = scd30.relative_humidity
            color_chase(GREEN, 0.01)
            color_chase(BLACK, 0.01)
        except Exception:
            pass
        c02_label.text = c02_text(co2)

        cognitive_function_label.text = cognitive_function_text(co2)
        (x, y, w, h) = cognitive_function_label.bounding_box
        cognitive_function_label.x = (120 - w // 2)

        if(max_co2 < co2):
            max_co2 = co2
            max_co2_label.text = max_co2_text(max_co2)
        else:
            max_co2_label.text = max_co2_text(max_co2)

        temp_and_humidity_label.text = temp_and_humidity_text(temp, relh)

        print("Co2: " + str(co2))
        print("Temp: " + str(temp))
        print("Humidity: " + str(relh))

    elif page == 1:
        c02_label.text = "page 2 top"
        cognitive_function_label.text = "page 2 middle"
        max_co2_label.text = "page 2 bottom"
        temp_and_humidity_label.text = temp_and_humidity_text(temp, relh)

    elif page == 2:
        c02_label.text = "page 3 top"
        cognitive_function_label.text = "page 3 middle"
        max_co2_label.text = "page 3 bottom"
        temp_and_humidity_label.text = temp_and_humidity_text(temp, relh)

    for time_left in range(100,0,-1):
        
        if touch_A2.value:
            page = 0
            continue
        elif touch_A3.value:
            page = 1
            continue
        elif touch_A4.value:
            page = 2
            continue

        refresh_label.text = refresh_text(time_left)

        time.sleep(0.01)
