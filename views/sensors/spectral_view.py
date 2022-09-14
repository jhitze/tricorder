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

def SpectralView(sensor, display_width, start_x, start_y):
    group = Group()
    base_width = 10
    width_to_show = display_width - start_x - base_width

    gap = 7
    violet_line = Rect(start_x,start_y + gap * 1, base_width + bar_graph(sensor.violet_415nm, width_to_show), gap, fill=violet)
    indigo_line = Rect(start_x,start_y + gap * 2, base_width + bar_graph(sensor.indigo_445nm, width_to_show), gap, fill=indigo)
    blue_line =   Rect(start_x,start_y + gap * 3, base_width + bar_graph(sensor.blue_480nm, width_to_show), gap, fill=blue)
    cyan_line =   Rect(start_x,start_y + gap * 4, base_width + bar_graph(sensor.cyan_515nm, width_to_show), gap, fill=cyan)
    green_line =  Rect(start_x,start_y + gap * 5, base_width + bar_graph(sensor.green_555nm, width_to_show), gap, fill=green)
    yellow_line = Rect(start_x,start_y + gap * 6, base_width + bar_graph(sensor.yellow_590nm, width_to_show), gap, fill=yellow)
    orange_line = Rect(start_x,start_y + gap * 7, base_width + bar_graph(sensor.orange_630nm, width_to_show), gap, fill=orange)
    red_line =    Rect(start_x,start_y + gap * 8, base_width + bar_graph(sensor.red_680nm, width_to_show), gap, fill=red)

    group.append(violet_line)
    group.append(indigo_line)
    group.append(blue_line)
    group.append(cyan_line)
    group.append(green_line)
    group.append(yellow_line)
    group.append(orange_line)
    group.append(red_line)

    return group

def bar_graph(read_value, display_width):
    scaled = int(arduino_map(read_value, 0, 65535, 0, display_width))
    return scaled

def arduino_map( x,  in_min,  in_max,  out_min,  out_max): 
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
