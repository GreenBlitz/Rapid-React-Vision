"""
Absolute camera.
"""
from subprocess import check_output

from gbvision import UNKNOWN_CAMERA

from constants import ports
import gbvision as gbv


# MOVE THIS TO GBRPI AFTER SEASON IS OVER
class AbsoluteUSBCamera(gbv.USBCamera):
    """
    Absolute camera.
    This is the same as USBCamera, but leverages a static hardware port.
    What this means is that if you access port 0, for example,
    it will definetly point to the first USB slot.
    """

    def __init__(self, absolute_port, data=UNKNOWN_CAMERA):
        path = f"realpath /dev/v4l/by-path/platform-fd500000.pcie-pci-0000\\:01\\:00.0-usb-0\\:1.{ports.USB_TO_VIDEO[absolute_port]}\:1.0-video-index0"
        video = check_output(path)
        super().__init__(video, data)
