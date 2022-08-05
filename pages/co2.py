import asyncio
from adafruit_display_text import label, wrap_text_to_lines
from adafruit_display_shapes.rect import Rect
import adafruit_scd30
from pages import *
from pages.page import Page

class Co2Page(Page):
    def __init__(self, display_width, i2c, neopixel):
        Page.__init__(self, display_width)
        self.max_co2 = 0
        self.co2 = 0
        self.temp = 0
        self.relh = 0.0
        self.neopixel = neopixel
        self.scd30 = adafruit_scd30.SCD30(i2c)
        self.scd30.measurement_interval = 5
        self.setup()
        self.setup_header()

    def setup(self):
        # Draw a top rectangle
        rect = Rect(0, 0, 240, 140, fill=BACKGROUND_COLOR)
        self.group.append(rect)

        # Draw a Foreground Rectangle
        rect = Rect(0, 50, 240, 140, fill=FOREGROUND_COLOR)
        self.group.append(rect)

        # Draw bottom rectangle
        rect = Rect(0, 190, 240, 140, fill=BACKGROUND_COLOR)
        self.group.append(rect)

        # Setup and Center the c02 Label
        self.co2_label = label.Label(font, text=" " * 20, line_spacing=1)
        self.co2_label.anchor_point = (0.5, 0)
        self.co2_label.anchored_position = (self.display_width /2, 50)
        self.co2_label.color = FOREGROUND_TEXT_COLOR
        self.co2_label.scale = defaultLabelScale
        self.group.append(self.co2_label)

        # Setup and Center the cognitive function Label
        self.cognitive_function_label = label.Label(font, text=" " * 20, line_spacing=.75)
        self.cognitive_function_label.anchor_point = (0.5, 0)
        self.cognitive_function_label.anchored_position = (self.display_width /2, 75)
        self.cognitive_function_label.color = FOREGROUND_TEXT_COLOR
        self.cognitive_function_label.scale = 2
        self.group.append(self.cognitive_function_label)

        # Setup and Center the max co2 Label
        self.max_co2_label = label.Label(font, text=" " * 20, line_spacing=1)
        self.max_co2_label.anchor_point = (0.5, 0)
        self.max_co2_label.anchored_position = (self.display_width /2, 125)
        self.max_co2_label.color = FOREGROUND_TEXT_COLOR
        self.max_co2_label.scale = defaultLabelScale
        self.group.append(self.max_co2_label)

        # Setup and Center the temp and humidity Label
        self.temp_and_humidity_label = label.Label(font, text=" " * 20, line_spacing=1)
        self.temp_and_humidity_label.anchor_point = (0.5, 0)
        self.temp_and_humidity_label.anchored_position = (self.display_width /2, 160)
        self.temp_and_humidity_label.color = FOREGROUND_TEXT_COLOR
        self.temp_and_humidity_label.scale = defaultLabelScale
        self.group.append(self.temp_and_humidity_label)

        # Setup and Center the refresh Label
        self.refresh_label = label.Label(font, text=" " * 20, line_spacing=1)
        self.refresh_label.anchor_point = (0.5, 0)
        self.refresh_label.anchored_position = (self.display_width /2, 200)
        self.refresh_label.color = BACKGROUND_TEXT_COLOR
        self.refresh_label.scale = defaultLabelScale
        self.group.append(self.refresh_label)

    async def check_sensor_readiness(self):
        self.neopixel = YELLOW
        while self.scd30.data_available != 1:
            await asyncio.sleep(0.5)
        self.neopixel = BLACK

    def update_values(self):
        try:
            self.co2 = self.scd30.CO2
            self.temp = self.scd30.temperature
            self.relh = self.scd30.relative_humidity
            self.neopixel = GREEN
            print("Co2: " + str(self.co2))
            print("Temp: " + str(self.temp))
            print("Humidity: " + str(self.relh))
        except Exception:
            self.neopixel = RED
            raise

        self.update_co2(self.co2)
        self.update_temp_and_relh(self.temp, self.relh)

    def update_co2(self, co2):
        self.co2 = co2
        self.update_cognitive_function_text(co2)
        self.update_max_co2(co2)
        self.co2_label.text = self.co2_text(co2)
    
    def update_max_co2(self, co2):
        if(self.max_co2 < co2):
            self.max_co2 = co2
            self.max_co2_label.text = self.max_co2_text(self.max_co2)
    
    def update_cognitive_function_text(self, co2):
        self.cognitive_function_label.text = self.cognitive_function_text(co2)
    
    def update_temp_and_relh(self, temp, relh):
        self.temp_and_humidity_label.text = self.temp_and_humidity_text(temp, relh)

    def co2_text(self, co2):
        return "CO2: {:.0f} PPM".format(co2)

    # Numbers from Kurtis Baute
    # https://www.youtube.com/watch?v=1Nh_vxpycEA
    # https://www.youtube.com/watch?v=PoKvPkwP4mM
    def cognitive_function_words(self, c02):
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

    def cognitive_function_text(self, co2):
        return "\n".join(wrap_text_to_lines(self.cognitive_function_words(co2), 20))

    def max_co2_text(self, max_co2_level):
        return "Max CO2: {:.0f} PPM".format(max_co2_level)

    def temp_and_humidity_text(self, temp, humidity):
        return "T:{:.2f}°C  H:{:.0f}%".format(temp, humidity)

    def refresh_text(self, time_left):
        return "Refresh in {}".format(time_left)
