from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_text import bitmap_label, wrap_text_to_lines
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

def Co2View(sensor, display_width, start_x, start_y):
    gc.collect()
    print( "Before co2view loaded Available memory: {} bytes".format(gc.mem_free()) )
    group = Group()
    width = 15
    height = 20
    radius = 4
    gap = 5
    padded_start_x = start_x + gap
    number_of_bars = int((display_width - gap*2) / (width + gap))
    # FONT.load_glyphs("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890.")
    # Label
    sensor_label = bitmap_label.Label(FONT, x=padded_start_x, y=start_y + gap*2, save_text = False, text="CO2")
    sensor_label.scale = 2
    sensor_label.color = WHITE
    group.append(sensor_label)

    start_y = start_y + gap + sensor_label.height

    # Value
    value_label = bitmap_label.Label(FONT, x=padded_start_x, y=start_y + gap*2, save_text = False, text="{0:6d} ppm".format(int(sensor.co2)))
    value_label.scale = 3
    value_label.color = WHITE
    group.append(value_label)

    start_y = start_y + gap*2 + value_label.height
    interpretation_label_background_color = BLACK
    i = 0
    while i < number_of_bars:
        display_range = sensor.danger_value() / number_of_bars
        color_bars = int(max(sensor.co2 - sensor.base_value(), 1) / display_range)

        fill_color = gray
        if sensor.co2 < sensor.warning_value() and i < color_bars:
            fill_color = green
            interpretation_label_background_color = green
        elif sensor.co2 < sensor.danger_value() and i < color_bars:
            fill_color = yellow
            interpretation_label_background_color = yellow
        elif sensor.co2 >= sensor.danger_value():
            fill_color = red
            interpretation_label_background_color = red
        roundrect = RoundRect(padded_start_x + ((width+gap) * i) + gap, start_y + gap , width, height, radius, fill=fill_color, stroke=2)
        group.append(roundrect)
        i += 1

    print("After bar Available memory: {} bytes".format(gc.mem_free()) )
    gc.collect()
    print("After bar GC Available memory: {} bytes".format(gc.mem_free()) )
    start_y = start_y + gap * 2 + height
    print("After bar start_y math Available memory: {} bytes".format(gc.mem_free()) )
    message_background = RoundRect(padded_start_x, start_y, display_width - gap*2, height * 2, radius, fill=interpretation_label_background_color)
    print("After background rect Available memory: {} bytes".format(gc.mem_free()) )
    group.append(message_background)

    # Text Interpretation
    interpretation_text = wrap_text_to_lines(sensor.cognitive_function_words(), 20)
    interpretation_label = bitmap_label.Label(FONT, 
                                       x=padded_start_x, 
                                       y=start_y + gap*3,
                                       padding_left = gap,
                                       padding_bottom = gap,
                                       save_text = False,
                                       text="\n".join(interpretation_text))
    interpretation_label.scale = 2
    interpretation_label.color = WHITE
    # interpretation_label.background_color = interpretation_label_background_color
    group.append(interpretation_label)

    start_y = start_y + gap*2 + interpretation_label.height
    return group
