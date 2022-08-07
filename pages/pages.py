import gc
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
        self.co2_page = Co2Page(self.display.width, self.i2c, self.pixels)
        print( "After Co2Page Loaded Available memory: {} bytes".format(gc.mem_free()) )
        # self.temperature_page = TemperaturePage(self.display.width)
        self.voc_page = VOCPage(self.display.width, self.i2c, self.pixels, self.co2_page)
        print( "After VOCPage Loaded Available memory: {} bytes".format(gc.mem_free()) )
        self.aq_page = AirParticulatePage(self.display.width, self.i2c, self.pixels)
        print( "After AirParticulatePage Loaded Available memory: {} bytes".format(gc.mem_free()) )
        self.current_page = self.co2_page
        self.__update_display__()
    
    def show_co2_page(self):
        self.current_page = self.co2_page
        self.__update_display__()
    
    def show_temperature_page(self):
        self.current_page = self.temperature_page
        self.__update_display__()
    
    def show_aq_page(self):
        self.current_page = self.aq_page
        self.__update_display__()

    def show_voc_page(self):
        self.current_page = self.voc_page
        self.__update_display__()
    
    def __update_display__(self):
        print("Page loaded:", self.current_page)
        self.display.show(self.current_page.group)
    