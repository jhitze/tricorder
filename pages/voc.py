import asyncio
from adafruit_display_text import label, wrap_text_to_lines
from adafruit_display_shapes.rect import Rect
from pages import *
from pages.page import Page
import adafruit_sgp30

class VOCPage(Page):
    def __init__(self, display_width, i2c, neopixels, co2_page):
        Page.__init__(self, display_width)
        self.co2_page = co2_page
        self.temp = 20
        self.relh = 20
        self.neopixels = neopixels
        self.pixel = 1
        self.i2c = i2c
        self.warmed_up = False
        
        self.setup_background()
        self.setup_header()
        self.setup_sensor()
    
    def setup_sensor(self):
        self.sgp30 = adafruit_sgp30.Adafruit_SGP30(self.i2c)
        print("SGP30 serial #", [hex(i) for i in self.sgp30.serial])
        self.sgp30.set_iaq_baseline(0x8973, 0x8AAE)
        self.__update_temp_and_relh__()
        

    def setup_background(self):
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
        self.tvoc_label = label.Label(font, text=" " * 20, line_spacing=1)
        self.tvoc_label.anchor_point = (0.5, 0)
        self.tvoc_label.anchored_position = (self.display_width /2, 50)
        self.tvoc_label.color = FOREGROUND_TEXT_COLOR
        self.tvoc_label.scale = defaultLabelScale
        self.group.append(self.tvoc_label)

        # Setup and Center the cognitive function Label
        self.cognitive_function_label = label.Label(font, text=" " * 20, line_spacing=.75)
        self.cognitive_function_label.anchor_point = (0.5, 0)
        self.cognitive_function_label.anchored_position = (self.display_width /2, 75)
        self.cognitive_function_label.color = FOREGROUND_TEXT_COLOR
        self.cognitive_function_label.scale = 2
        self.group.append(self.cognitive_function_label)

        # Setup and Center the refresh Label
        self.refresh_label = label.Label(font, text=" " * 20, line_spacing=1)
        self.refresh_label.anchor_point = (0.5, 0)
        self.refresh_label.anchored_position = (self.display_width /2, 200)
        self.refresh_label.color = BACKGROUND_TEXT_COLOR
        self.refresh_label.scale = defaultLabelScale
        self.group.append(self.refresh_label)

    def set_pixel_color(self, color):
        self.neopixels[self.pixel] = color
        self.neopixels.show()
    
    async def check_sensor_readiness(self):
        self.set_pixel_color(YELLOW)
        try:
            while not self.warmed_up and self.sgp30.eCO2 == 0:
                self.update_refresh_text("Sensor Warming Up")
                print("warming_voc_up", self.warmed_up, self.sgp30.TVOC)
                await asyncio.sleep(0.5)
        except Exception:
            self.warmed_up = False
            print("exception", Exception)
        self.warmed_up = True
        self.set_pixel_color(BLACK)

    async def update_values(self):
        self.update_refresh_text("Reading from sensor")
        try:
            self.__update_temp_and_relh__()
            self.tvoc = self.sgp30.TVOC
            self.set_pixel_color(GREEN)
            print("TVOC: " + str(self.tvoc))
            self.set_pixel_color(BLACK)
        except Exception:
            self.neopixels[0] = RED
            raise

        self.update_tvoc()
        await asyncio.sleep(.5)

    def __update_temp_and_relh__(self):
        if(self.temp != self.co2_page.temp and self.relh != self.co2_page.relh):
            self.temp = self.co2_page.temp
            self.relh = self.co2_page.relh
            print("Seting tvoc sensor's temp and hum:", self.temp, self.relh)
            self.sgp30.set_iaq_relative_humidity(celsius=self.temp, relative_humidity=self.relh)

    def update_tvoc(self):
        self.tvoc_label.text = self.tvoc_text(self.tvoc)

    def tvoc_text(self, tvoc):
        return "TVOC: {:.0f} PPB".format(tvoc)
    
    def update_refresh_text(self, text):
        self.refresh_label.text = text

    def cognitive_function_text(self, co2):
        return "\n".join(wrap_text_to_lines(self.cognitive_function_words(co2), 20))

    def temp_and_humidity_text(self, temp, humidity):
        return "T:{:.2f}°C  H:{:.0f}%".format(temp, humidity)
