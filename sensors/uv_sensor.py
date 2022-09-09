import adafruit_ltr390

class UVSensor():
    def __init__(self, i2c):
        self.i2c = i2c
        self.uv = 0
        self.uv_index = 0

    def setup(self):
        self.ltr = adafruit_ltr390.LTR390(self.i2c)

    async def check_sensor_readiness(self):
        pass

    async def update_values(self):
        self.uv = self.ltr.uvs
        self.uv_index = self.ltr.uvi
        print("UV raw: {0}".format(self.uv))
        print("UV Index: {0}".format(self.uv_index))

    def text(self):
        lines = []
        lines.append("UV Index: {0}".format(self.uv_index))
        lines.append("UV raw: {0}".format(self.uv))
        text = "\n".join(lines)
        return text
