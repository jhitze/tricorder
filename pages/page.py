from displayio import Group
from adafruit_display_text import bitmap_label

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
BLACK = (0,0,0)


### new display idea
BACKGROUND_COLOR = 0xFF0000
FOREGROUND_COLOR = 0xFFFFFF
BACKGROUND_TEXT_COLOR = 0xFFFFFF
FOREGROUND_TEXT_COLOR = 0x000000

defaultLabelScale = 2

class Page:
    def __init__(self, display_width):
        self.display_width = display_width
        self.group = Group()

    def setup_header(self):
        # Setup and Center the header label
        # self.header_label = bitmap_label.Label(FONT, save_text = False, text="Cheap-o Tricorder")
        # self.header_label.color = BACKGROUND_TEXT_COLOR
        # self.header_label.scale = defaultLabelScale
        # self.header_label.anchor_point = (0.5, 0)
        # self.header_label.anchored_position = (self.display_width /2, 10)
        # self.group.append(self.header_label)
        pass
    
    async def check_sensor_readiness(self):
        pass

    async def update_values(self):
        pass
