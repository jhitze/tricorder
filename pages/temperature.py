from adafruit_display_shapes.rect import Rect
from pages import *
from pages.page import Page


class TemperaturePage(Page):
    def __init__(self, display_width):
        Page.__init__(self, display_width)
        self.setup()
        self.setup_header()

    def setup(self):
        # Draw a top rectangle
        rect = Rect(0, 0, 240, 140, fill=BLACK)
        self.group.append(rect)

        # Draw a Foreground Rectangle
        rect = Rect(0, 50, 240, 140, fill=YELLOW)
        self.group.append(rect)

        # Draw bottom rectangle
        rect = Rect(0, 190, 240, 140, fill=BLACK)
        self.group.append(rect)
    
    




