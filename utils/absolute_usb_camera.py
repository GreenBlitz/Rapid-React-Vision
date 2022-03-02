import subprocess

from gbvision import UNKNOWN_CAMERA

from constants import ports
import gbvision as gbv
class absolute_usb_camera(gbv.USBCamera):

	def __init__(self, absolute_port, data=UNKNOWN_CAMERA):
		path = f"realpath /dev/v4l/by-path/platform-fd500000.pcie-pci-0000\\:01\\:00.0-usb-0\\:1.{ports.USB_TO_VIDEO[absolute_port]}\:1.0-video-index0 "
		video = subprocess.check_output(path)
		super().__init__(video, data)
