
from pages.co2 import Co2Page
from pages.temperature import TemperaturePage


class Pages():
    def __init__(self, i2c, pixels, display):
        self.display = display
        self.i2c = i2c
        self.pixels = pixels
        self.co2_page = Co2Page(self.display.width, i2c, pixels)
        self.temperature_page = TemperaturePage(self.display.width)
        self.current_page = self.co2_page
        self.__update_display__()
    
    def show_co2_page(self):
        self.current_page = self.co2_page
        self.__update_display__()
    
    def show_temperature_page(self):
        self.current_page = self.temperature_page
        self.__update_display__()
    
    def __update_display__(self):
        print("Page loaded:", self.current_page)
        self.display.show(self.current_page.group)
    