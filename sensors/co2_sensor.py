import asyncio
import adafruit_scd30
from sensors.sensor import Sensor
from adafruit_display_text import wrap_text_to_lines

class Co2Sensor(Sensor):
    def __init__(self, i2c):
        Sensor.__init__(self)
        self.i2c = i2c
        self.max_co2 = 0
        self.co2 = 0
        self.temp = 0
        self.relh = 0.0
    
    def setup(self):
        self.scd30 = adafruit_scd30.SCD30(self.i2c)
        self.scd30.measurement_interval = 5

    async def check_sensor_readiness(self):
        while self.scd30.data_available != 1:
            await asyncio.sleep(0.5)

    async def update_values(self):
        self.co2 = self.scd30.CO2
        self.temp = self.scd30.temperature
        self.relh = self.scd30.relative_humidity
        print("co2: ", self.co2)
        print("temp: ", self.temp)
        print("relh: ", self.relh)
    
    def text(self):
        lines = []
        lines.append(self.co2_text(self.co2))
        for line in self.cognitive_function_text(self.co2):
            lines.append(line)
        lines.append(self.max_co2_text(self.co2))
        lines.append(self.temp_and_humidity_text(self.temp, self.relh))
        text = "\n".join(lines)
        return text
    
    def co2_text(self, co2):
        return "CO2: {:.0f} PPM".format(co2)

    # Numbers from Kurtis Baute
    # https://www.youtube.com/watch?v=1Nh_vxpycEA
    # https://www.youtube.com/watch?v=PoKvPkwP4mM
    def cognitive_function_words(self, c02):
        if(c02 > 39000):
            return "Death Possible"
        elif(c02 >= 10000):
            return "Long Term Health Risk"
        elif(c02 >= 2000):
            return "Physical Problems Possible"
        elif(c02 >= 1400):
            return "50% Cognitive Decrease"
        elif(c02 >= 1000):
            return "15% Cognitive Decrease"
        elif(c02 > 500):
            return "Above outside levels"
        else:
            return "Outside level ~411ppm"

    def cognitive_function_text(self, co2):
        return wrap_text_to_lines(self.cognitive_function_words(co2), 20)
    
    def max_co2_text(self, max_co2_level):
        return "Max CO2: {:.0f} PPM".format(max_co2_level)

    def temp_and_humidity_text(self, temp, humidity):
        return "T:{:.2f}°C  H:{:.0f}%".format(temp, humidity)

    def base_value(self):
        return 500
    
    def warning_value(self):
        return 1000
    
    def danger_value(self):
        return 1400