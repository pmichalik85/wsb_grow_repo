import time
import board
import busio
import adafruit_ads1x15.ads1115 as ads1115
from adafruit_ads1x15.analog_in import AnalogIn


class AdcADS1x15():
    def __init__(self, channel):
        self.i2c = board.I2C()
        self.ads1115 = ads1115.ADS1115(self.i2c)
        self.chan = AnalogIn(self.ads1115, ads1115.P0)

    def convert(self):
        return self.chan.value