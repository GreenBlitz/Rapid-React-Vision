# all exposure constants go in this file
from tools import is_on_rpi

__is_on_rpi = is_on_rpi()

HIGH_EXPOSURE = 11 if __is_on_rpi else -3
LOW_EXPOSURE = 10 if __is_on_rpi else -10

AUTO_EXPOSURE_ON = True
AUTO_EXPOSURE_OFF = False
