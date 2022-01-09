"""
Algorithm to locate the upper hub of the 2 hubs in the center of the map.
"""
from typing import Union, Iterable

import gbrpi
import gbvision as gbv

from algorithms import BaseAlgorithm
from constants import LOW_EXPOSURE
from vision_master import LedRing


class FindHub(BaseAlgorithm):
	"""
	Identify the reflectors on the upper hub and in doing so, locate the hub.
	"""

	def _process(self, frame: gbv.Frame, camera: gbv.Camera) -> Union[
		gbrpi.ConnEntryValue, Iterable[gbrpi.ConnEntryValue]]:
		pass

	def reset(self, camera: gbv.Camera, led_ring: LedRing):
		camera.set_auto_exposure(False)
		camera.set_exposure(LOW_EXPOSURE)
		led_ring.on()
