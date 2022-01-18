"""
Algorithm to locate the upper hub of the 2 hubs in the center of the map.
"""
from typing import Union, Iterable, Tuple, Dict, List

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

	# noinspection PySameParameterValue,PyMethodMayBeStatic
	def __get_closest_locations(self, locations, count: int):
		"""
		Gets the closest locations out of a list of locations.

		:param locations: The list of locations.
		:param count: The amount of minimums to get (e.g., the 2 closest points)
		:return:
		"""
		# List of points
		minimums: List[gbv.Location] = []

		# Convert to a dict like so: {distance: location_object}
		distance_to_point: Dict[float, gbv.Location] = {}

		# For each location
		for loc in locations:
			# Get the distance and add it to the dict
			distance_to_point[gbv.plane_distance_from_object(loc)] = loc

		# For the amount of minimums to find
		for i in range(count):
			# Get the minimum distance using min(), this will return a key
			# Pop the key's value from the dict
			minimums.append(distance_to_point.pop(min(distance_to_point)))

		return minimums
