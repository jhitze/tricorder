import asyncio
import adafruit_sgp30
from adafruit_display_text import wrap_text_to_lines
from sensors.sensor import Sensor

class VOCSensor(Sensor):
    def __init__(self, i2c, co2_page):
        self.i2c = i2c
        self.co2_page = co2_page
        self.warmed_up = False
        self.tvoc = 0
        self.temp = 20
        self.relh = 20

    def setup(self):
        self.sgp30 = adafruit_sgp30.Adafruit_SGP30(self.i2c)
        print("SGP30 serial #", [hex(i) for i in self.sgp30.serial])
        self.sgp30.set_iaq_baseline(0x8973, 0x8AAE)
        self.__update_temp_and_relh__()

    async def check_sensor_readiness(self):
        try:
            while not self.warmed_up and self.sgp30.eCO2 == 0:
                self.update_refresh_text("Sensor Warming Up")
                print("warming_voc_up", self.warmed_up, self.sgp30.TVOC)
                await asyncio.sleep(0.5)
        except Exception as e:
            self.warmed_up = False
            print("exception:", e)
            pass

        self.warmed_up = True

    async def update_values(self):
        self.__update_temp_and_relh__()
        self.tvoc = self.sgp30.TVOC
        print("TVOC: " + str(self.tvoc))
    
    def __update_temp_and_relh__(self):
        if(self.temp != self.co2_page.temp and self.relh != self.co2_page.relh):
            self.temp = self.co2_page.temp
            self.relh = self.co2_page.relh
            print("Seting tvoc sensor's temp and hum:", self.temp, self.relh)
            try:
                self.sgp30.set_iaq_relative_humidity(celsius=self.temp, relative_humidity=self.relh)
            except OSError as ex:
                print("Error updating sgp30: {}".format(ex))

    def text(self):
        lines = []
        lines.append(self.tvoc_text(self.tvoc))
        lines.append("")
        for line in self.interpretation_text(self.tvoc):
            lines.append(line)
        text = "\n".join(lines)
        return text

    def tvoc_text(self, tvoc):
        return "TVOC: {:.0f} PPB".format(tvoc)
    
    def interpretation(self, tvoc):
        if tvoc < 250:
            return "The VOC contents in the air are low."
        elif tvoc >= 250 and tvoc < 2000:
            return "The VOC is not good."
        elif tvoc >= 2000:
            return "The VOC contents are very high. Leave now."
    
    def interpretation_text(self, tvoc):
        return wrap_text_to_lines(self.interpretation(tvoc), 20)
