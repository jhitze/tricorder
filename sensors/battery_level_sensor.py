from adafruit_lc709203f import LC709203F
from sensors.sensor import Sensor

class BatteryLevelSensor(Sensor):
    def __init__(self, i2c):
        self.i2c = i2c
        self.cell_percent = 0
        self.pack_size = 0

    def setup(self):
        self.battery = LC709203F(self.i2c)

    async def check_sensor_readiness(self):
        pass

    async def update_values(self):
        self.cell_percent = self.battery.cell_percent
        self.pack_size = self.battery.pack_size
        print("Cell Pack: {0}".format(self.cell_percent))
        print("Cell Percent {0}%".format(self.pack_size))

    def text(self):
        lines = []
        lines.append("Cell Pack: {0}".format(self.cell_percent))
        lines.append("Cell Percent {0}%".format(self.pack_size))
        text = "\n".join(lines)
        return text
