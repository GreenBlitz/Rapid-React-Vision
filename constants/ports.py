"""
all ports constants go in this file
"""
from typing import Dict

from tools import is_on_rpi

import subprocess as sp
import glob
import re

DEV_CAMERA_PORT = 1
LED_RING_PORT = 18
USB_TO_VIDEO = {
"top right": 1,
"top left": 3,
"bottom right": 2,
"bottom left": 4
}

LOC_TO_USB = {
    "FRONT" : "bottom_right",
    "????" : "????"
}

