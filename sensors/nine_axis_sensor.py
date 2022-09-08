import asyncio
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL

class NineAxisSensor():
    def __init__(self, i2c):
        self.i2c = i2c

    def setup(self):
        self.accel_gyro = LSM6DS(self.i2c)
        self.mag = LIS3MDL(self.i2c)

    async def check_sensor_readiness(self):
        pass

    async def update_values(self):

        self.acceleration = self.accel_gyro.acceleration
        self.gyro = self.accel_gyro.gyro
        self.magnetic = self.mag.magnetic
        print("Acceleration: X:{0:3.0f}, Y:{1:3.0f}, Z:{2:3.0f} m/s^2".format(*self.acceleration))
        print("Gyro          X:{0:3.0f}, Y:{1:3.0f}, Z:{2:3.0f} rad/s".format(*self.gyro))
        print("Magnetic      X:{0:3.0f}, Y:{1:3.0f}, Z:{2:3.0f} uT".format(*self.magnetic))


    def text(self):
        lines = []
        lines.append("Acceleration X:{0:3.0f}, Y:{1:3.0f}, Z:{2:3.0f} m/s^2".format(*self.acceleration))
        lines.append("Gyro         X:{0:3.0f}, Y:{1:3.0f}, Z:{2:3.0f} rad/s".format(*self.gyro))
        lines.append("Magnetic     X:{0:3.0f}, Y:{1:3.0f}, Z:{2:3.0f} uT".format(*self.magnetic))
        text = "\n".join(lines)
        return text
