# all ports constants go in this file
from tools import is_on_rpi

import subprocess as sp
import glob
import re

__is_on_rpi = is_on_rpi()
CAMERA_PORT = 1
INTERFACE_TO_LOC = {
    "03000002": "FRONT",
    "03000005": "BACK",
    "???": "SHOOTER"
}

INTERFACE_REGEX = re.compile("Interface Info:\n\tID\s+: 0x(\d+)", re.M)


def generate_camera_ports():
    final_dict = {}
    ports = glob.glob("/dev/video*")
    for port in ports:
        pipe = sp.Popen(["v4l2-ctl", "--all", "--device", port], stdout=sp.PIPE)
        info = (pipe.communicate()[0]).decode()
        interface_id = INTERFACE_REGEX.findall(info)[-1]
        if interface_id in list(INTERFACE_TO_LOC.keys()):
            final_dict[INTERFACE_TO_LOC[interface_id]] = int(port[10:])
        pipe.terminate()
    return final_dict

LED_RING_PORT = 18
