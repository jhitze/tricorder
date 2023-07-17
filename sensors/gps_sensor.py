import asyncio
import adafruit_gps
from sensors.sensor import Sensor

class GPSSensor(Sensor):
    def __init__(self, i2c):
        self.i2c = i2c

    def setup(self):
        self.gps = adafruit_gps.GPS_GtopI2C(self.i2c, debug=False)
        # Turn on the basic GGA and RMC info (what you typically want)
        self.gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
        # Update every second
        self.gps.send_command(b"PMTK220,2000")

    async def check_sensor_readiness(self):
        if(self.gps.update()):
            return
        print("waiting on gps update")
        await asyncio.sleep(0.5)

    async def update_values(self):
        print("Updating gps values")
        if not self.gps.has_fix:
            # Try again if we don't have a fix yet.
            print("Waiting for fix...")
            return

    def text(self):
        lines = []
        if not self.gps.has_fix:
            lines.append("No fix yet...")
        else:
            lines.append("Fix quality: {}".format(self.gps.fix_quality))
            if self.gps.satellites is not None:
                lines.append("# satellites: {}".format(self.gps.satellites))
            lines.append("Lat: {:2.}d{:2.4f}m".format(
                self.gps.latitude_degrees, self.gps.latitude_minutes))
            lines.append("Long: {:2.}d{:2.4f}m".format(
                self.gps.longitude_degrees, self.gps.longitude_minutes))
            if self.gps.speed_knots is not None:
                lines.append("Speed: {} knots".format(self.gps.speed_knots))
            if self.gps.altitude_m is not None:
                lines.append("Altitude: {} m".format(self.gps.altitude_m))
        text = "\n".join(lines)
        return text
