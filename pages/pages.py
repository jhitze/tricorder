import gc

from pages.sensor_page import SensorPage
print( "Before pages.co2 in Code Loaded Available memory: {} bytes".format(gc.mem_free()) )
from pages.co2 import Co2Page
print( "After pages.co2 in Code Loaded Available memory: {} bytes".format(gc.mem_free()) )
# from pages.temperature import TemperaturePage
from pages.voc import VOCPage
print( "After pages.voc in Code Loaded Available memory: {} bytes".format(gc.mem_free()) )
from pages.air_particulate import AirParticulatePage
print( "After pages.air_particulate in Code Loaded Available memory: {} bytes".format(gc.mem_free()) )
import gc

class Pages():
    def __init__(self, i2c, pixels, display):
        self.start_mem = gc.mem_free()
        print( "Before Pages Available memory: {} bytes".format(self.start_mem) ) 
        self.display = display
        self.i2c = i2c
        self.pixels = pixels
        self.sensor_page = SensorPage(self.display.width, self.i2c, self.pixels)
        self.current_page = self.sensor_page
        self.__update_display__()
    
    def show_sensor_page(self):
        self.current_page = self.show_sensor_page
        self.__update_display__()
    
    def __update_display__(self):
        print("Page loaded:", self.current_page)
        self.display.show(self.current_page.group)
    