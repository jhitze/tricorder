import gc
from pages.sensor_page import SensorPage

class Pages():
    def __init__(self, i2c, display):
        self.start_mem = gc.mem_free()
        print( "Before Pages Available memory: {} bytes".format(self.start_mem) ) 
        self.display = display
        self.i2c = i2c
        self.sensor_page = SensorPage(self.display.width, self.i2c)
        self.current_page = self.sensor_page
        self.__update_display__()
    
    def show_sensor_page(self):
        self.current_page = self.sensor_page
        self.__update_display__()
    
    def next(self):
        self.current_page.next()
    
    def previous(self):
        self.current_page.previous()
    
    def goto_page(self, number):
        return self.current_page.goto_page(number)
    
    def option_clicked(self):
        self.current_page.option_clicked()
    
    def __update_display__(self):
        print("Page loaded:", self.current_page)
        self.display.show(self.current_page.group)
    