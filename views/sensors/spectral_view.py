from adafruit_display_shapes.rect import Rect
from displayio import Group

violet = 0xee82ee
indigo = 0x4b0082
blue = 0x0000ff
cyan =  0x00ffff
green = 0x008000 
yellow = 0xFFFF00
orange = 0xffa500 
red = 0xff0000 

class SpectralView:
    def __init__(self, sensor, display_width, start_x, start_y):
        self.group = Group()
        self.sensor = sensor
        self.base_width = 10
        self.width_to_show = display_width - start_x - self.base_width
        self.start_x = start_x
        self.start_y = start_y
        self.gap = 7
    
    def group(self):
        return self.group
    
    def update(self):
        while len(self.group) > 0:
            self.group.pop()

        violet_line = Rect(self.start_x, self.start_y + self.gap * 1, self.base_width + self.bar_graph(self.sensor.violet_415nm, self.width_to_show) , self.gap, fill=violet)
        indigo_line = Rect(self.start_x, self.start_y + self.gap * 2, self.base_width + self.bar_graph(self.sensor.indigo_445nm, self.width_to_show) , self.gap, fill=indigo)
        blue_line =   Rect(self.start_x, self.start_y + self.gap * 3, self.base_width + self.bar_graph(self.sensor.blue_480nm, self.width_to_show) , self.gap, fill=blue)
        cyan_line =   Rect(self.start_x, self.start_y + self.gap * 4, self.base_width + self.bar_graph(self.sensor.cyan_515nm, self.width_to_show) , self.gap, fill=cyan)
        green_line =  Rect(self.start_x, self.start_y + self.gap * 5, self.base_width + self.bar_graph(self.sensor.green_555nm, self.width_to_show) , self.gap, fill=green)
        yellow_line = Rect(self.start_x, self.start_y + self.gap * 6, self.base_width + self.bar_graph(self.sensor.yellow_590nm, self.width_to_show) , self.gap, fill=yellow)
        orange_line = Rect(self.start_x, self.start_y + self.gap * 7, self.base_width + self.bar_graph(self.sensor.orange_630nm, self.width_to_show) , self.gap, fill=orange)
        red_line =    Rect(self.start_x, self.start_y + self.gap * 8, self.base_width + self.bar_graph(self.sensor.red_680nm, self.width_to_show) , self.gap, fill=red)
    
        self.group.append(violet_line)
        self.group.append(indigo_line)
        self.group.append(blue_line)
        self.group.append(cyan_line)
        self.group.append(green_line)
        self.group.append(yellow_line)
        self.group.append(orange_line)
        self.group.append(red_line)


    def bar_graph(self, read_value, display_width):
        scaled = int(self.arduino_map(read_value, 0, 65535, 0, display_width))
        return scaled
    
    def arduino_map(self, x,  in_min,  in_max,  out_min,  out_max): 
      return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    