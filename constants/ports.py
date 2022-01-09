# all ports constants go in this file
from tools import is_on_rpi

__is_on_rpi = is_on_rpi()

CAMERA_PORT = 0 if __is_on_rpi else 1

LED_RING_PORT = 18
