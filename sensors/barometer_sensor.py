import asyncio
import adafruit_bmp3xx
from adafruit_display_text import wrap_text_to_lines
from sensors.sensor import Sensor

class BarometerSensor(Sensor):
    def __init__(self, i2c):
        self.i2c = i2c
        self.pressure = 0
        self.temp = 20
        self.altitude = 20
        self.sea_level_pressure = 1013.25

    def setup(self):
        self.bmp = adafruit_bmp3xx.BMP3XX_I2C(self.i2c)
        self.bmp.pressure_oversampling = 8
        self.bmp.temperature_oversampling = 2


    async def check_sensor_readiness(self):
        pass

    async def update_values(self):
        self.temp = self.bmp.temperature
        self.pressure = self.bmp.pressure
        self.altitude = self.bmp.altitude
        print("Pressure: {:6.4f}  Altitude: {:5.2f}".format(self.pressure, self.altitude))

    def text(self):
        lines = []
        lines.append(self.pressure_text(self.pressure))
        lines.append(self.altitude_text(self.altitude))
        lines.append("")
        for line in self.interpretation_text(self.pressure):
            lines.append(line)
        text = "\n".join(lines)
        return text

    def pressure_text(self, pressure):
        return "Pressure: {:4.2f} mb".format(pressure)
    
    def altitude_text(self, altitude):
        return "Altitude: {:5.2f} m".format(altitude)
    
    def interpretation_text(self, pressure):
        return wrap_text_to_lines(self.interpretation(pressure), 20)
    
    def interpretation(self, pressure):
        if pressure < 1009.144:
            return "Low Pressure/ Rainy Weather"
        elif pressure >= 1009.144 and pressure < 1022.689:
            return "Normal Pressure/ Steady Weather"
        elif pressure >= 1022.689:
            return "High Pressure/ Calm Weather"
    
    
