import asyncio
from pages.page import Page
# from pages import FONT
from sensors.air_particulate_sensor import AirParticulateSensor
from sensors.barometer_sensor import BarometerSensor
from sensors.co2_sensor import Co2Sensor
from sensors.spectral_sensor import SpectralSensor
from sensors.uv_sensor import UVSensor
from sensors.voc_sensor import VOCSensor
from sensors.nine_axis_sensor import NineAxisSensor
from views.sensors.co2_view import Co2View
from views.sensors.spectral_view import SpectralView
# from displayio import Group
# from adafruit_display_text import label


RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
BLACK = (0,0,0)
WHITE = (255, 255, 255)




class SensorPage(Page):
    def __init__(self, display_width, i2c):
        Page.__init__(self, display_width)
        self.i2c = i2c
        self.pixel = 0
        self.current_sensor = None
        self.current_sensor_index = 0
        # self.display_group = Group()
        # self.default_view_group = Group()
        self.current_view = None
        self.all_sensors = []
        self.setup_areas()
        self.setup_header()
        self.create_sensors()

    def setup_areas(self):
        # Draw a top rectangle
        # rect = Rect(0, 0, 240, 140, fill=BACKGROUND_COLOR)
        # self.group.append(rect)

        # Draw a Foreground Rectangle
        # rect = Rect(0, 50, 240, 140, fill=FOREGROUND_COLOR)
        # self.group.append(rect)

        # Setup and Center the c02 Label
        # self.sensor_text_label = label.Label(FONT, text=" " * 20, line_spacing=1)
        # self.sensor_text_label.anchor_point = (0.5, 0)
        # self.sensor_text_label.anchored_position = (self.display_width /2, 50)
        # self.sensor_text_label.color = WHITE
        # self.sensor_text_label.scale = 2
        # self.default_view_group.append(self.sensor_text_label)
        
        # self.display_group.append(self.default_view_group)
        # self.group.append(self.display_group)
        pass

    
    def create_sensors(self):
        self.co2Sensor = Co2Sensor(self.i2c)
        self.co2Sensor.setup()
        self.all_sensors.append(self.co2Sensor)
        
        self.airParticulateSensor = AirParticulateSensor(self.i2c)
        self.airParticulateSensor.setup()
        self.all_sensors.append(self.airParticulateSensor)

        # self.vocSensor = VOCSensor(self.i2c, self.co2Sensor)
        # try:
        #     self.vocSensor.setup()
        # except Exception as ex:
        #     print("VOC sensor failed to setup. - {0}".format(ex))
        
        # self.all_sensors.append(self.vocSensor)

        self.barometerSensor = BarometerSensor(self.i2c)
        self.barometerSensor.setup()
        self.all_sensors.append(self.barometerSensor)

        self.spectralSensor = SpectralSensor(self.i2c)
        self.spectralSensor.setup()
        self.all_sensors.append(self.spectralSensor)

        self.nineAxisSensor = NineAxisSensor(self.i2c)
        self.nineAxisSensor.setup()
        self.all_sensors.append(self.nineAxisSensor)

        self.uvSensor = UVSensor(self.i2c)
        self.uvSensor.setup()
        self.all_sensors.append(self.uvSensor)

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
        try:
            await self.current_sensor.check_sensor_readiness()
            await self.current_sensor.update_values()

            if type(self.current_sensor) == SpectralSensor:
                print("Using SpectralView")
                self.group = SpectralView(self.current_sensor, self.display_width, 0,50)
            elif type(self.current_sensor) == Co2Sensor:
                print("Using co2 view")
                if type(self.current_view) != Co2View:
                    self.current_view = Co2View(self.current_sensor, self.display_width, 0, 0)
                    self.current_view.create_ui()
                    self.group = self.current_view.group
                
            else:
                print("Using DefaultView with nothing in it")
                # group = self.default_view_group
                # self.update_text(self.current_sensor.text())
            
            self.current_view.update()
            
            await asyncio.sleep(0.5)
        except Exception as e:
            print("exception:", e)
            await asyncio.sleep(.5)
            raise

