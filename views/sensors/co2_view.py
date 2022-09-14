from adafruit_display_shapes.roundrect import RoundRect
import displayio

violet = 0xee82ee
indigo = 0x4b0082
blue = 0x0000ff
cyan =  0x00ffff
green = 0x32cd32
yellow = 0xFFFF00
orange = 0xffa500 
red = 0xff0000 
gray = 0x808080

def Co2View(sensor, display_width, start_x, start_y):
    group = displayio.Group()
    width = 15
    height = 20
    radius = 4
    gap = 5
    width_left = display_width
    padded_start_x = start_x + gap
    print("Starting width_left:", width_left)
    number_of_bars = int((display_width - gap*2) / (width + gap))
    print("number of bars", number_of_bars)

    for i in range(number_of_bars):
        display_range = sensor.danger_value() / number_of_bars
        color_bars = int(max(sensor.co2 - sensor.base_value(), 1) / display_range)

        fill_color = gray
        if sensor.co2 < sensor.warning_value() and i < color_bars:
            fill_color = green
        elif sensor.co2 < sensor.danger_value() and i < color_bars:
            fill_color = yellow
        elif sensor.co2 >= sensor.danger_value():
            fill_color = red
        roundrect = RoundRect(padded_start_x + ((width+gap) * i) + gap, start_y + gap , width, height, radius, fill=fill_color, stroke=2)
        group.append(roundrect)
    
    return group
