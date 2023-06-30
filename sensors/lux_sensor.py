import adafruit_tsl2591
from sensors.sensor import Sensor

class LuxSensor(Sensor):
    def __init__(self, i2c):
        self.i2c = i2c
        self.uv = 0
        self.uv_index = 0

    def setup(self):
        self.tsl = adafruit_tsl2591.TSL2591(self.i2c)

    async def check_sensor_readiness(self):
        pass

    async def update_values(self):
        self.infrared = self.tsl.infrared
        self.visible = self.tsl.visible
        self.lux = self.tsl.lux
        print("Infrared: {0}".format(self.infrared))
        print("Visible: {0}".format(self.visible))
        print("Lux: {0}".format(self.lux))

    def text(self):
        lines = []
        lines.append("Infrared: {0}".format(self.infrared))
        lines.append("Visible: {0}".format(self.visible))
        lines.append("Lux: {0}".format(self.lux))
        text = "\n".join(lines)
        return text
