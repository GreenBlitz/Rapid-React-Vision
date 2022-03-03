"""
Absolute camera.
"""
import gbvision as gbv
from gbvision import UNKNOWN_CAMERA
from subprocess import check_output
from constants import USB_TO_VIDEO


# MOVE THIS TO GBRPI AFTER SEASON IS OVER


class AbsoluteUSBCamera(gbv.USBCamera):
    """
    Absolute camera.
    This is the same as USBCamera, but leverages a static hardware port.
    What this means is that if you access port 0, for example,
    it will definetly point to the first USB slot.
    """

    def __init__(self, absolute_port: str, data=UNKNOWN_CAMERA):
        # Format the command
        path = f"/dev/v4l/by-path/platform-fd500000.pcie-pci-0000\\:01\\:00.0-usb-0\\:1.{USB_TO_VIDEO[absolute_port]}\:1.0-video-index0"
        # Run the command
        output = check_output(f"realpath {path}")
        # If the video file was found
        if path == output:
            raise FileNotFoundError(f"Camera stream {USB_TO_VIDEO[absolute_port]} not found.")
        else:
            super().__init__(output[10:], data)
