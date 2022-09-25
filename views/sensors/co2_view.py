from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_text.label import Label
from displayio import Group
from terminalio import FONT
import gc

violet = 0xee82ee
indigo = 0x4b0082
blue = 0x0000ff
cyan =  0x00ffff
green = 0x32cd32
yellow = 0xFFFF00
orange = 0xffa500 
red = 0xff0000 
gray = 0x808080
BLACK = (0,0,0)
WHITE = (255, 255, 255)

class Co2View:
    def __init__(self, sensor, display_width, start_x, start_y):
        gc.collect()
        print(start_x, start_y)
        self.group = Group()
        self.width = 15
        self.height = 20
        self.radius = 4
        self.gap = 5
        self.padded_start_x = start_x + self.gap
        self.start_y = start_y
        self.number_of_bars = int((display_width - self.gap*2) / (self.width + self.gap))
        self.sensor = sensor
        self.bars = []
        print("co2view init done")
    
    def create_ui(self):
        print("co2view create_ui")
        # Label
        sensor_label = Label(FONT, x=self.padded_start_x, y=self.start_y + self.gap*2, text="CO2")
        sensor_label.scale = 2
        sensor_label.color = WHITE
        self.group.append(sensor_label)

        self.start_y = self.start_y + self.gap + sensor_label.height

        # Value
        self.value_label = Label(FONT, x=self.padded_start_x, y=self.start_y + self.gap*2, text="{0:6d} ppm".format(0))
        self.value_label.scale = 3
        self.value_label.color = WHITE
        self.group.append(self.value_label)

        self.start_y = self.start_y + self.gap*2 + self.value_label.height
        interpretation_label_background_color = BLACK
        
        i = 0
        while i < self.number_of_bars:
            
            roundrect = RoundRect(self.padded_start_x + ((self.width+self.gap) * i) + self.gap, self.start_y + self.gap , self.width, self.height, self.radius, fill=gray, stroke=2)
            self.bars.append(roundrect)
            self.group.append(roundrect)
            i += 1
    
        self.start_y = self.start_y + self.gap * 2 + self.height

        # Text Interpretation
        self.interpretation_label = Label(FONT, 
                                        x=self.padded_start_x, 
                                        y=self.start_y + self.gap*3,
                                        padding_left = self.gap,
                                        padding_bottom = self.gap,
                                        text=self.sensor.cognitive_function_words())
        self.interpretation_label.scale = 2
        self.interpretation_label.color = WHITE
        self.interpretation_label.background_color = interpretation_label_background_color
        self.group.append(self.interpretation_label)

        self.start_y = self.start_y + self.gap*2 + self.interpretation_label.height
        return self.group

    def update(self):
        print("co2view update - {} bars".format(len(self.bars)))
        i = 0
        for bar in self.bars:
            display_range = self.sensor.danger_value() / self.number_of_bars
            color_bars = int(max(self.sensor.co2 - self.sensor.base_value(), 1) / display_range)

            fill_color = gray
            if self.sensor.co2 < self.sensor.warning_value() and i < color_bars:
                fill_color = green
                interpretation_label_background_color = green
            elif self.sensor.co2 < self.sensor.danger_value() and i < color_bars:
                fill_color = yellow
                interpretation_label_background_color = yellow
            elif self.sensor.co2 >= self.sensor.danger_value():
                fill_color = red
                interpretation_label_background_color = red
            bar.fill = fill_color
            i += 1
        
        self.value_label.text = "{0:6d} ppm".format(int(self.sensor.co2))
        self.interpretation_label.background_color = interpretation_label_background_color
        self.interpretation_label.text = self.sensor.cognitive_function_words()