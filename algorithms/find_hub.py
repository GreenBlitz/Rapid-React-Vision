"""
Algorithm to locate the upper hub of the 2 hubs in the center of the map.
"""
from typing import Union, Iterable

import gbrpi
import gbvision as gbv

from algorithms import BaseAlgorithm
from constants import LOW_EXPOSURE, UPPER_HUB, CONTOUR_MIN_AREA, UPPER_HUB_THRESHOLD
from vision_master import LedRing


class FindHub(BaseAlgorithm):
	"""
	Identify the reflectors on the upper hub and in doing so, locate the hub.
	"""
	algorithm_name = 'hub'

	def __init__(self, output_key, success_key, conn, log_algorithm_incomplete=False):
		BaseAlgorithm.__init__(self, output_key, success_key, conn, log_algorithm_incomplete)
		self.finder = gbv.CircleFinder(game_object=UPPER_HUB, threshold_func=UPPER_HUB_THRESHOLD,
		                               contour_min_area=CONTOUR_MIN_AREA)

	def _process(self, frame: gbv.Frame, camera: gbv.Camera) -> Union[
		gbrpi.ConnEntryValue, Iterable[gbrpi.ConnEntryValue]]:
		pass

	def reset(self, camera: gbv.Camera, led_ring: LedRing):
		camera.set_auto_exposure(False)
		camera.set_exposure(LOW_EXPOSURE)
		led_ring.on()
