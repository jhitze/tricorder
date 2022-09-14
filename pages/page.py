import displayio
from adafruit_display_text import bitmap_label
from pages import *


class Page:
    def __init__(self, display_width):
        self.display_width = display_width
        self.group = displayio.Group()

    def setup_header(self):
        # Setup and Center the header label
        self.header_label = bitmap_label.Label(FONT, save_text = False, text="Cheap-o Tricorder")
        self.header_label.color = BACKGROUND_TEXT_COLOR
        self.header_label.scale = defaultLabelScale
        self.header_label.anchor_point = (0.5, 0)
        self.header_label.anchored_position = (self.display_width /2, 10)
        self.group.append(self.header_label)
    
    async def check_sensor_readiness(self):
        pass

    async def update_values(self):
        pass
