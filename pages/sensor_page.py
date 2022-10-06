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
from views.sensors.air_particulate_view import AirParticulateView
from views.sensors.co2_view import Co2View
from views.sensors.spectral_view import SpectralView
from adafruit_display_shapes.roundrect import RoundRect
from displayio import Group
from adafruit_display_text import label
from adafruit_displayio_layout.layouts.tab_layout import TabLayout
from terminalio import FONT
import board

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
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
        self.start_y = 0
        self.gap = 5
        self.current_sensor = None
        self.current_sensor_index = 0
        self.sensor_display_group = Group()
        self.current_view = None
        self.all_sensors = []
        self.header_objects=0
        self.setup_areas()
        self.setup_header()
        self.create_sensors()

    def setup_areas(self):
        # Draw a top rectangle
        # rect = Rect(0, 0, 240, 140, fill=YELLOW)
        roundrect = RoundRect(0 + self.gap, self.start_y + self.gap , self.display_width - (self.gap * 2), 36, 15, fill=YELLOW)
        self.group.append(roundrect)
        self.header_objects += 1
        # self.start_y = self.start_y + roundrect.height

        # Draw a Foreground Rectangle
        # rect = Rect(0, 50, 240, 140, fill=FOREGROUND_COLOR)
        # self.group.append(rect)

        # Setup and Center the Header
        self.header_text = label.Label(FONT, text="Tricorder", x=self.display_width - 200, y=self.start_y + (self.gap *5) - 2)
        self.header_text.color = YELLOW
        self.header_text.background_color = BLACK
        self.header_text.scale = 3
        self.group.append(self.header_text)
        self.header_objects +=1
        self.start_y = self.start_y + roundrect.height
        
        # roundrect = RoundRect(0 + self.gap, self.start_y , 40, 400, 15, fill=YELLOW)
        # self.group.append(roundrect)
        # self.header_objects += 1

        self.test_page_layout = TabLayout(
                            x=0,
                            y=self.start_y + self.gap,
                            display=board.DISPLAY,
                            tab_text_scale=2,
                            custom_font=FONT,
                            inactive_tab_spritesheet="bmps/inactive_tab_sprite.bmp",
                            showing_tab_spritesheet="bmps/active_tab_sprite.bmp",
                            showing_tab_text_color=BLUE,
                            inactive_tab_text_color=YELLOW,
                            inactive_tab_transparent_indexes=(0, 1),
                            showing_tab_transparent_indexes=(0, 1),
                            tab_count=4,
                        )

        
       
        self.group.append(self.test_page_layout)
        self.start_y = self.start_y + self.test_page_layout.tab_height
        self.header_objects += 1
    
    def create_sensors(self):
        
        
        self.co2Sensor = Co2Sensor(self.i2c)
        self.co2Sensor.setup()
        self.all_sensors.append(self.co2Sensor)

        self.co2view = Co2View(self.co2Sensor, self.display_width, 0, self.gap)
        self.co2view.create_ui()                    
        self.test_page_layout.add_content(self.co2view.group, "CO2")
        
        self.airParticulateSensor = AirParticulateSensor(self.i2c)
        self.airParticulateSensor.setup()
        self.all_sensors.append(self.airParticulateSensor)
        self.airParticulateView = AirParticulateView(self.airParticulateSensor, self.display_width, 0, self.gap)
        self.test_page_layout.add_content(self.airParticulateView.group, "PM")

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
        self.spectral_view = SpectralView(self.spectralSensor, self.display_width, 0, self.gap)
        self.test_page_layout.add_content(self.spectral_view.group, "Spectral")

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
                # self.group = SpectralView(self.current_sensor, self.display_width, 0,50)
                self.test_page_layout.show_page(page_name="Spectral")
                self.spectral_view.update()
            elif type(self.current_sensor) == Co2Sensor:
                print("Using co2 view")
                self.test_page_layout.show_page(page_name="CO2")
                self.co2view.update()
            elif type(self.current_sensor) == AirParticulateSensor:
                print("using air particulate view")
                self.test_page_layout.show_page(page_name="PM")
                self.airParticulateView.update()
                
            else:
                print("Using DefaultView with nothing in it")
                # group = self.default_view_group
                # self.update_text(self.current_sensor.text())
            
            # self.current_view.update()
            
            # await asyncio.sleep(0.5)
        except Exception as e:
            print("exception:", e)
            await asyncio.sleep(.5)
            raise

