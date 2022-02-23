"""
all ports constants go in this file
"""
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

INTERFACE_REGEX = re.compile(r"Interface Info:\n\tID\s+: 0x(\d+)", re.M)


def generate_camera_ports():
    """
    Maps the hardware ports to virtual ports.

    For example the first USB slot goes
    to /dev/video1, the second USB slot maps to /dev/video4...

    :return: A dictionary of matching names of some form
            (for example, "FRONT_CAMERA") to their mapped
            stream port/file (such as /dev/video1).
    """
    # Init the dictionary to return
    final_dict = {}
    # Get all the files in /dev/ which are called video* ('video' with any text after it)
    ports = glob.glob("/dev/video*")
    # For each file found (stream)
    for port in ports:
        try:
            # Get all the information about this port
            # Run the following command to get it
            pipe = sp.Popen(["v4l2-ctl", "--all", "--device", port], stdout=sp.PIPE)
            # Get the data that the command returned
            # If the command does not respond within the timeout, then terminate it.
            info = (pipe.communicate(timeout=10)[0]).decode()
            # Close the program if it's still open for whatever reason
            pipe.terminate()
            # Use RegEx to get the ID of the port
            interface_id = INTERFACE_REGEX.findall(info)[-1]
            # If this ID is a valid camera ID
            if interface_id in list(INTERFACE_TO_LOC.keys()):
                # Map our temporary name to the virtual port
                # For example, {FRONT_CAMERA : /dev/video1}
                # What this means is that in the end, we have a dictionary where
                # we know exactly which camera points to what file stream.
                final_dict[INTERFACE_TO_LOC[interface_id]] = int(port[10:])
        except sp.TimeoutExpired as e:
            print(f"Popen failed with error: {e}")
    # Return the output dictionary
    return final_dict

LED_RING_PORT = 18
