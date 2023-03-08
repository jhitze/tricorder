from adafruit_display_shapes.rect import Rect
from adafruit_display_text.label import Label
from adafruit_display_shapes.circle import Circle
from displayio import Group
from terminalio import FONT

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

class AirParticulateView:
    def __init__(self, sensor, display_width, start_x, start_y):
        self.group = Group()
        self.sensor = sensor
        self.base_width = 10
        self.width_to_show = display_width - start_x - self.base_width
        self.start_x = start_x
        self.start_y = start_y
        self.gap = 7
        
        print("Making circle")
        circle_one = Circle(self.start_x + 20, self.start_y, 21, fill=orange)
        self.group.append(circle_one)

        self.start_y += 50
        self.start_x += 50

        print("Making label")
        # Value
        self.pm_1_0_value_label = Label(FONT, 
                                    x=self.start_x + 40, 
                                    y=self.start_y + self.gap*2,
                                    background_tight = False,
                                    padding_top = 10,
                                    padding_bottom = 2,
                                    padding_left = 40,
                                    padding_right = 5,
                                    text="PM 1.0")
        self.pm_1_0_value_label.scale = 2
        self.pm_1_0_value_label.color = BLACK
        self.pm_1_0_value_label.background_color = yellow
        self.group.append(self.pm_1_0_value_label)

        # Value
        print("Making label 2")
        align_x = self.pm_1_0_value_label.width + self.gap + 130
        self.pm_1_0_value = Label(FONT, x=self.start_x + align_x, y=self.start_y + self.gap*2, text="0")
        self.pm_1_0_value.scale = 3
        self.pm_1_0_value.color = orange
        self.group.append(self.pm_1_0_value)

        self.start_y = self.start_y + self.gap*2 + self.pm_1_0_value_label.height + 30

        self.pm_2_5_value_label = Label(FONT, 
                                    x=self.start_x + 40, 
                                    y=self.start_y + self.gap*2,
                                    background_tight = False,
                                    padding_top = 10,
                                    padding_bottom = 2,
                                    padding_left = 40,
                                    padding_right = 5,
                                    text="PM 2.5")
        self.pm_2_5_value_label.scale = 2
        self.pm_2_5_value_label.color = BLACK
        self.pm_2_5_value_label.background_color = yellow
        self.group.append(self.pm_2_5_value_label)


        # Value
        print("Making label 3")
        align_x = self.pm_2_5_value_label.width + self.gap + 130
        self.pm_2_5_value = Label(FONT, x=self.start_x + align_x, y=self.start_y + self.gap*2, text="0")
        self.pm_2_5_value.scale = 3
        self.pm_2_5_value.color = orange
        self.group.append(self.pm_2_5_value)
        
        self.start_y = self.start_y + self.gap*2 + self.pm_1_0_value_label.height + 30

        print("Making label 4")
        self.pm_10_value_label = Label(FONT, 
                                    x=self.start_x + 40, 
                                    y=self.start_y + self.gap*2,
                                    background_tight = False,
                                    padding_top = 10,
                                    padding_bottom = 2,
                                    padding_left = 40,
                                    padding_right = 5,
                                    text="PM  10")
        self.pm_10_value_label.scale = 2
        self.pm_10_value_label.color = BLACK
        self.pm_10_value_label.background_color = yellow
        self.group.append(self.pm_10_value_label)


        # Value
        print("Making label 5")
        align_x = self.pm_10_value_label.width + self.gap + 130
        self.pm_10_value = Label(FONT, x=self.start_x + align_x, y=self.start_y + self.gap*2, text="0")
        self.pm_10_value.scale = 3
        self.pm_10_value.color = orange
        self.group.append(self.pm_10_value)

        print("Done with init.")
    
    def group(self):
        return self.group
    
    def update(self):
        self.pm_1_0_value.text = "{:0>3.0f}".format(self.sensor.pm1p0)
        self.pm_2_5_value.text = "{:0>3.0f}".format(self.sensor.pm2p5)
        self.pm_10_value.text  = "{:0>3.0f}".format(self.sensor.pm10)
