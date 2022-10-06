import asyncio
from adafruit_pm25.i2c import PM25_I2C
from sensors.sensor import Sensor

class AirParticulateSensor(Sensor):
    def __init__(self, i2c):
        self.i2c = i2c
        self.reset_pin = None
        self.pm2p5 = 0
        self.max_pm2p5 = 0
        self.pm1p0 = 0
        self.pm10 = 0

    def setup(self):
        self.pm25Sensor = PM25_I2C(self.i2c, self.reset_pin)

    async def check_sensor_readiness(self):
        pass

    async def update_values(self):
        try:
            self.aqdata = self.pm25Sensor.read()
        except Exception as ex:
            print("Failed reading data.", ex)
            return
        print("pm: " + str(self.aqdata))
        self.pm2p5 = self.aqdata["pm25 standard"]
        self.pm1p0 = self.aqdata["pm10 standard"]
        self.pm10 = self.aqdata["pm100 standard"]
        if self.pm2p5 > self.max_pm2p5:
            self.max_pm2p5 = self.pm2p5
        await asyncio.sleep(0.5)

    def text(self):
        lines = []
        lines.append(self.pm2p5_text(self.pm2p5))
        lines.append(self.pm1p0_text(self.pm1p0))
        lines.append(self.pm10_text(self.pm10))
        lines.append(self.interpretation(self.max_pm2p5))
        text = "\n".join(lines)
        return text

    def pm1p0_text(self, pm1p0):
        return "PM 1.0: {:.0f}".format(pm1p0)

    def pm2p5_text(self, pm2p5):
        return "PM 2.5: {:.0f}".format(pm2p5)
    
    def pm10_text(self, pm10):
        return "PM  10: {:.0f}".format(pm10)
    
    def interpretation(self, pm2p5):
        if(pm2p5 > 12):
            return "PM2.5 is too high!"
        elif(self.max_pm2p5 > 35):
            return "You need to leave"
        else:
            return "Seems Okay"
