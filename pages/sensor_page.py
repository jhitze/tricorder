import asyncio
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from pages import *
from pages.page import Page
from sensors.air_particulate_sensor import AirParticulateSensor
from sensors.co2_sensor import Co2Sensor

class SensorPage(Page):
    def __init__(self, display_width, i2c, neopixels):
        Page.__init__(self, display_width)
        self.i2c = i2c
        self.neopixels = neopixels
        self.pixel = 0
        self.current_sensor = None
        self.all_sensors = []
        self.setup_areas()
        self.setup_header()
        self.create_sensors()

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
    
    def create_sensors(self):
        self.co2Sensor = Co2Sensor(self.i2c)
        self.co2Sensor.setup()
        self.all_sensors.append(self.co2Sensor)
        self.airParticulateSensor = AirParticulateSensor(self.i2c)
        self.airParticulateSensor.setup()
        self.all_sensors.append(self.airParticulateSensor)
        self.current_sensor = self.all_sensors[0]
    
    def next(self):
        self.current_sensor = self.all_sensors[1]
    
    def previous(self):
        self.current_sensor = self.all_sensors[0]

    async def run(self):
        while True:
            try:
                self.set_pixel_color(YELLOW)
                await self.current_sensor.check_sensor_readiness()
                await self.current_sensor.update_values()
                self.set_pixel_color(GREEN)
                self.update_text(self.current_sensor.text())
                self.set_pixel_color(BLACK)
                await asyncio.sleep(0.5)
            except Exception as e:
                self.set_pixel_color(RED)
                print("exception:", e)
                await asyncio.sleep(.5)
                raise
    

    def update_text(self, text):
        self.sensor_text_label.text = text

