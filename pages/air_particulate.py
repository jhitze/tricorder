import asyncio
from adafruit_display_text import label, wrap_text_to_lines
from adafruit_display_shapes.rect import Rect
from pages import BACKGROUND_COLOR, BLACK, FOREGROUND_COLOR, FOREGROUND_TEXT_COLOR, BACKGROUND_TEXT_COLOR, GREEN, RED, YELLOW, font, defaultLabelScale

from pages.page import Page


class AirParticulatePage(Page):
    def __init__(self, display_width, i2c, neopixels):
        Page.__init__(self, display_width)
        self.neopixels = neopixels
        self.pixel = 2
        self.i2c = i2c
        self.reset_pin = None
        
        self.setup_background()
        self.setup_header()
        self.setup_sensor()
    
    def setup_sensor(self):
        self.pm25 = PM25_I2C(self.i2c, self.reset_pin)
        
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
        self.pm25_label = label.Label(font, text=" " * 20, line_spacing=1)
        self.pm25_label.anchor_point = (0.5, 0)
        self.pm25_label.anchored_position = (self.display_width /2, 50)
        self.pm25_label.color = FOREGROUND_TEXT_COLOR
        self.pm25_label.scale = defaultLabelScale
        self.group.append(self.pm25_label)

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
            while self.sgp30.eCO2 == 0:
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
            self.aqdata = self.pm25.read()
            self.set_pixel_color(GREEN)
            print("pm: " + str(self.aqdata))
            self.set_pixel_color(BLACK)
        except Exception:
            self.neopixels[0] = RED
            raise
        
        self.update_pm25()
        await asyncio.sleep(.5)

    def update_pm25(self):
        self.pm25_label.text = self.pm25_text(self.aqdata["pm25 standard"])

    def pm25_text(self, tvoc):
        return "PM 2.5: {:.0f}".format(tvoc)
    
    def update_refresh_text(self, text):
        self.refresh_label.text = text

    def update_voc_interpretation(self):
        interpretation = self.interpretation()
        self.cognitive_function_label.text = "\n".join(wrap_text_to_lines(interpretation, 20))
    
    def interpretation(self):
        if self.tvoc < 250:
            return "The VOC contents in the air are low."
        elif self.tvoc >= 250 and self.tvoc < 2000:
            return "The VOC is not good."
        elif self.tvoc >= 2000:
            return "The VOC contents are very high leave now."
