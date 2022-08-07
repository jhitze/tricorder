import asyncio
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from pages import *
from pages.page import Page

class SensorPage(Page):
    def __init__(self, display_width, neopixels):
        Page.__init__(self, display_width)
        self.neopixels = neopixels
        self.pixel = 0
        self.current_sensor_index = 0
        self.sensors = []
        
        self.setup_areas()
        self.setup_header()
        self.setup_sensors()

    def setup_areas(self):
        # Draw a top rectangle
        rect = Rect(0, 0, 240, 140, fill=BACKGROUND_COLOR)
        self.group.append(rect)

        # Draw a Foreground Rectangle
        rect = Rect(0, 50, 240, 140, fill=FOREGROUND_COLOR)
        self.group.append(rect)

        # Setup and Center the c02 Label
        self.sensor_text_label = label.Label(font, text=" " * 20, line_spacing=1)
        self.sensor_text_label.anchor_point = (0.5, 0)
        self.sensor_text_label.anchored_position = (self.display_width /2, 50)
        self.sensor_text_label.color = FOREGROUND_TEXT_COLOR
        self.sensor_text_label.scale = defaultLabelScale
        self.group.append(self.sensor_text_label)

    def set_pixel_color(self, color):
        self.neopixels[self.pixel] = color
        self.neopixels.show()
    
    def setup_sensors():
        pass

    async def run(self):
        while True:
            current_sensor = self.sensors[self.current_sensor_index]
            try:
                self.set_pixel_color(YELLOW)
                await current_sensor.check_sensor_readiness()
                await current_sensor.update_values()
                self.set_pixel_color(GREEN)
                self.update_text(current_sensor.text())
            except:
                self.set_pixel_color(RED)
                await asyncio.sleep(.5)
                pass
    

    def update_text(self, text):
        self.sensor_text_label.text = text

