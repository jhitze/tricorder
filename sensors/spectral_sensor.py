import asyncio
from adafruit_as7341 import AS7341
from adafruit_display_text import wrap_text_to_lines

class SpectralSensor():
    def __init__(self, i2c):
        self.i2c = i2c
        self.violet_415nm = 0
        self.indigo_445nm = 0
        self.blue_480nm   = 0
        self.cyan_515nm   = 0
        self.green_555nm  = 0
        self.yellow_590nm = 0
        self.orange_630nm = 0
        self.red_680nm    = 0
        self.light_needed = False

    def setup(self):
        self.sensor = AS7341(self.i2c)
        self.sensor.led_current = 25
        self.sensor.led = False

    async def check_sensor_readiness(self):
        pass

    def option_clicked(self):
        print("Changing light status")
        self.light_needed = not self.light_needed

    async def update_values(self):
        if self.light_needed:
            print("enabling led to read colors")
            self.sensor.led = True
        self.violet_415nm  = self.sensor.channel_415nm
        self.indigo_445nm  = self.sensor.channel_445nm
        self.blue_480nm    = self.sensor.channel_480nm
        self.cyan_515nm    = self.sensor.channel_515nm
        self.green_555nm   = self.sensor.channel_555nm
        self.yellow_590nm  = self.sensor.channel_590nm
        self.orange_630nm  = self.sensor.channel_630nm
        self.red_680nm     = self.sensor.channel_680nm
        if self.sensor.led:
            print("disabling led")
            self.sensor.led = False
        print("415nm/Violet  %s" % self.violet_415nm)
        print("445nm/Indigo %s" % self.indigo_445nm)
        print("480nm/Blue   %s" % self.blue_480nm)
        print("515nm/Cyan   %s" % self.cyan_515nm)
        print("555nm/Green   %s" % self.green_555nm)
        print("590nm/Yellow  %s" % self.yellow_590nm)
        print("630nm/Orange  %s" % self.orange_630nm)
        print("680nm/Red     %s" % self.red_680nm)

    def text(self):
        lines = []
        lines.append(self.top_wavelength_text())
        lines.append("")
        lines.append("")
        text = "\n".join(lines)
        return text

    def top_wavelength_text(self):
        top_wavelength = self.highest_wavelength()
        return "Top wavelength {}".format(top_wavelength)
    
    def highest_wavelength(self):
        allwaves = self.all_wavelengths()
        brightest = 0
        brightest_name = "None"
        for name, value in allwaves.items():
            if value > brightest:
                brightest_name = name
                brightest = value

        return brightest_name

    def all_wavelengths(self):
        allwaves = {
            "415nm/Violet" : self.violet_415nm,
            "445nm/Indigo" : self.indigo_445nm,
            "480nm/Blue" : self.blue_480nm,
            "515nm/Cyan" : self.cyan_515nm,
            "555nm/Green" : self.green_555nm,
            "590nm/Yellow" : self.yellow_590nm,
            "630nm/Orange" : self.orange_630nm,
            "680nm/Red" : self.red_680nm
        }
        return allwaves
