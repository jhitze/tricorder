import asyncio
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
from pages import *
from pages.page import Page
from sensors.air_particulate_sensor import AirParticulateSensor
from sensors.barometer_sensor import BarometerSensor
from sensors.co2_sensor import Co2Sensor
from sensors.spectral_sensor import SpectralSensor
from sensors.uv_sensor import UVSensor
# from sensors.voc_sensor import VOCSensor
from sensors.lux_sensor import LuxSensor
from sensors.nine_axis_sensor import NineAxisSensor
from sensors.battery_level_sensor import BatteryLevelSensor
from sensors.gps_sensor import GPSSensor
from views.sensors.spectral_view import SpectralView
import displayio
import gc

class SensorPage(Page):
    def __init__(self, display_width, i2c):
        Page.__init__(self, display_width)
        self.i2c = i2c
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
        rect = Rect(0, 0, 240, 40, fill=BACKGROUND_COLOR)
        self.group.append(rect)

        # Setup and Center the c02 Label
        self.sensor_text_label = label.Label(font, text=" " * 20, line_spacing=1)
        self.sensor_text_label.anchor_point = (0.5, 0)
        self.sensor_text_label.anchored_position = (self.display_width /2, 50)
        self.sensor_text_label.color = BACKGROUND_TEXT_COLOR
        self.sensor_text_label.scale = defaultLabelScale
        self.default_view_group.append(self.sensor_text_label)

        self.display_group.append(self.default_view_group)
        self.group.append(self.display_group)


    def create_sensors(self):
        self.co2Sensor = Co2Sensor(self.i2c)
        self.co2Sensor.setup()
        self.all_sensors.append(self.co2Sensor)
        gc.collect()

        self.airParticulateSensor = AirParticulateSensor(self.i2c)
        self.airParticulateSensor.setup()
        self.all_sensors.append(self.airParticulateSensor)
        gc.collect()

        # self.vocSensor = VOCSensor(self.i2c, self.co2Sensor)
        # try:
        #     self.vocSensor.setup()
        # except Exception as ex:
        #     print("VOC sensor failed to setup. - {0}".format(ex))

        # self.all_sensors.append(self.vocSensor)

        self.barometerSensor = BarometerSensor(self.i2c)
        self.barometerSensor.setup()
        self.all_sensors.append(self.barometerSensor)
        gc.collect()

        self.spectralSensor = SpectralSensor(self.i2c)
        self.spectralSensor.setup()
        self.all_sensors.append(self.spectralSensor)
        gc.collect()

        self.nineAxisSensor = NineAxisSensor(self.i2c)
        self.nineAxisSensor.setup()
        self.all_sensors.append(self.nineAxisSensor)
        gc.collect()

        self.uvSensor = UVSensor(self.i2c)
        self.uvSensor.setup()
        self.all_sensors.append(self.uvSensor)
        gc.collect()

        self.luxSensor = LuxSensor(self.i2c)
        self.luxSensor.setup()
        self.all_sensors.append(self.luxSensor)
        gc.collect()

        self.batterySensor = BatteryLevelSensor(self.i2c)
        self.batterySensor.setup()
        self.all_sensors.append(self.batterySensor)
        gc.collect()

        self.gpsSensor = GPSSensor(self.i2c)
        self.gpsSensor.setup()
        self.all_sensors.append(self.gpsSensor)
        gc.collect()

        self.current_sensor = self.all_sensors[0]

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

    def sensor_count(self):
        return len(self.all_sensors)

    def goto_page(self, number):
        page_index = number
        if page_index < 0:
            page_index = 0
        elif page_index >= self.sensor_count():
            page_index = self.sensor_count() - 1

        self.current_sensor = self.all_sensors[page_index]
        print("Sensor set page to #{}".format(page_index))

        return page_index

    def option_clicked(self):
        self.current_sensor.option_clicked()

    async def run(self):
        while True:
            try:
                await self.current_sensor.check_sensor_readiness()
                gc.collect()
                await self.current_sensor.update_values()
                gc.collect()
                if type(self.current_sensor) == SpectralSensor:
                    print("Using SpectralView")
                    group = SpectralView(self.current_sensor, self.display_width, 0,50)
                else:
                    print("Using DefaultView")
                    group = self.default_view_group
                    gc.collect()
                    self.update_text(self.current_sensor.text())

                self.display_group.pop()
                gc.collect()
                self.display_group.append(group)
                gc.collect()
                await asyncio.sleep(0.5)
            except Exception as e:
                print("exception2:", e)
                await asyncio.sleep(.5)
                raise


    def update_text(self, text):
        self.sensor_text_label.text = text

