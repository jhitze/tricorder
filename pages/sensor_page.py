import asyncio
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from pages import *
from pages.page import Page
from sensors.air_particulate_sensor import AirParticulateSensor
from sensors.barometer_sensor import BarometerSensor
from sensors.co2_sensor import Co2Sensor
from sensors.spectral_sensor import SpectralSensor
from sensors.voc_sensor import VOCSensor
from sensors.nine_axis_sensor import NineAxisSensor
from views.sensors.spectral_view import SpectralView
import displayio

class SensorPage(Page):
    def __init__(self, display_width, i2c, neopixels):
        Page.__init__(self, display_width)
        self.i2c = i2c
        self.neopixels = neopixels
        self.pixel = 0
        self.current_sensor = None
        self.current_sensor_index = 0
        self.display_group = displayio.Group()
        self.default_view_group = displayio.Group()
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
        self.default_view_group.append(self.sensor_text_label)
        
        self.display_group.append(self.default_view_group)
        self.group.append(self.display_group)

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

        self.vocSensor = VOCSensor(self.i2c, self.co2Sensor)
        self.vocSensor.setup()
        self.all_sensors.append(self.vocSensor)

        self.barometerSensor = BarometerSensor(self.i2c)
        self.barometerSensor.setup()
        self.all_sensors.append(self.barometerSensor)

        self.spectralSensor = SpectralSensor(self.i2c)
        self.spectralSensor.setup()
        self.all_sensors.append(self.spectralSensor)

        self.nineAxisSensor = NineAxisSensor(self.i2c)
        self.nineAxisSensor.setup()
        self.all_sensors.append(self.nineAxisSensor)

        self.current_sensor = self.all_sensors[5]
    
    def next(self):
        self.current_sensor_index = self.current_sensor_index + 1
        if self.current_sensor_index >= len(self.all_sensors):
            self.current_sensor_index = 0
        
        print("Sensor Index: ", self.current_sensor_index)
        self.current_sensor = self.all_sensors[self.current_sensor_index]
    
    def previous(self):
        self.current_sensor_index = self.current_sensor_index - 1
        if self.current_sensor_index < 0:
            self.current_sensor_index = len(self.all_sensors) - 1
        
        print("Sensor Index: ", self.current_sensor_index)
        self.current_sensor = self.all_sensors[self.current_sensor_index]

    async def run(self):
        while True:
            try:
                self.set_pixel_color(YELLOW)
                await self.current_sensor.check_sensor_readiness()
                await self.current_sensor.update_values()
                self.set_pixel_color(GREEN)
                if type(self.current_sensor) == SpectralSensor:
                    print("Using SpectralView")
                    group = SpectralView(self.current_sensor, self.display_width, 0,50)
                else:
                    print("Using DefaultView")
                    group = self.default_view_group
                    self.update_text(self.current_sensor.text())
                
                self.display_group.pop()
                self.display_group.append(group)
                self.set_pixel_color(BLACK)
                await asyncio.sleep(0.5)
            except Exception as e:
                self.set_pixel_color(RED)
                print("exception:", e)
                await asyncio.sleep(.5)
                raise
    

    def update_text(self, text):
        self.sensor_text_label.text = text

