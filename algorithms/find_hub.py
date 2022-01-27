"""
Algorithm to locate the upper hub of the 2 hubs in the center of the map.
"""
from gbvision import Location, Number
from typing import Union, Iterable, Tuple, Dict, List, Optional

import gbrpi
import gbvision as gbv
from math import hypot as distance, sqrt

from algorithms import BaseAlgorithm
from constants import LOW_EXPOSURE, REFLECTOR_TAPE, CONTOUR_MIN_AREA, REFLECTOR_THRESHOLD, UPPER_HUB_RADIUS
from vision_master import LedRing


# noinspection PyUnusedClass
class FindHub(BaseAlgorithm):
	"""
	Identify the reflectors on the upper hub and in doing so, locate the hub.
	"""
	algorithm_name = 'hub'

	def __init__(self, output_key, success_key, conn, log_algorithm_incomplete=False):
		BaseAlgorithm.__init__(self, output_key, success_key, conn, log_algorithm_incomplete)
		self.finder = gbv.RectFinder(
			game_object=REFLECTOR_TAPE,
			threshold_func=REFLECTOR_THRESHOLD,
			contour_min_area=CONTOUR_MIN_AREA
		)

	def _process(self, frame: gbv.Frame, camera: gbv.Camera) -> Union[
		gbrpi.ConnEntryValue, Iterable[gbrpi.ConnEntryValue]]:
		# Get all the markers on the hoop
		shapes = self.finder.find_shapes(frame)

		# We have to be able to see at least 2 markers for the algorithm to work
		# (Uses the calculation of a circle center by 2 points and a fixed radius)
		if len(shapes) < 2:
			raise self.AlgorithmIncomplete()

		# Convert each shape to a location in 3D space.
		real_locations = self.finder.locations_from_shapes(shapes, camera)

		# We need to get the 2 closest markers, since they will be the most accurate
		# I made this abstract function in case later we want to change it to
		# finding the circle center with 3 points and no radius or something similar.
		mins = self.__get_closest_locations(real_locations, 2)

		# Get the hoop's center (X, Z)
		center = self.__get_circle_center(mins[0], mins[1])

		# If the center was found
		if center:
			# Return with any Y value (the hoop is parallel to the ground plane, so all points have the same Y)
			print(center[0], mins[0][1], center[1])
			return center[0], mins[0][1], center[1]
		else:
			raise self.AlgorithmIncomplete()

	def reset(self, camera: gbv.Camera, led_ring: LedRing) -> None:
		"""
		Reset the camera. Also runs on initiation.
		"""
		camera.set_auto_exposure(False)
		camera.set_exposure(LOW_EXPOSURE)
		led_ring.on()

	# noinspection PyMethodMayBeStatic,DuplicatedCode
	def __get_both_centers(self, x1_: float, y1_: float, x2_: float, y2_: float, radius_: float) -> \
		Optional[Tuple[Tuple[Number, Number], Tuple[Number, Number]]]:
		"""
		~ Three poor kids spent a few hours
		~ trying to solve, but to no arousal
		~ a question so difficult, it may seem,
		~ that it even stumped the Cyber team.

		~ And after years of hard labor,
		~ did they finally come to savor
		~ that when our brains sweat and glow,
		~ do we all turn to Stack Overflow.


		TLDR: A lot of math.
		See: https://stackoverflow.com/q/36211171/11985743
		:return If it finds both possible center points, then it returns ((X_1, Z_1), (X_2, Z_2)).
				Otherwise, returns None.
		"""
		radsq = radius_ ** 2

		a = sqrt((x2_ - x1_) ** 2 + (y2_ - y1_) ** 2)

		if radsq - (a / 2) ** 2 < 0:
			print(f"Something went wrong: {radsq - (a / 2) ** 2}")
			return

		b = sqrt(radsq - (a / 2) ** 2)

		ba_ratio = b / a

		x3 = (x1_ + x2_) / 2
		y3 = (y1_ + y2_) / 2

		bay_delta = ba_ratio * (y1_ - y2_)
		bax_delta = ba_ratio * (x1_ - x2_)

		# +-, so return both possible centers.
		# The format is ((X_1, Z_1), (X_2, Z_2))
		return ((x3 - bay_delta,
		         y3 + bax_delta),
		        (x3 + bay_delta,
		         y3 - bax_delta))

	def __get_circle_center(self, point1: Location, point2: Location) -> Optional[Tuple[gbv.Number, gbv.Number]]:
		"""
		Takes 2 points and calculates the center of the circle (x, z)
		that lies on them, given a fixed radius.
		"""
		# Get the centers
		cents = self.__get_both_centers(point1[0], point1[2], point2[0], point2[2], UPPER_HUB_RADIUS)
		# If it did not find both centers (camera bugs)
		if not cents:
			return
		# Return the center that is farther away
		# If '#' is hoop, '*' is markers, 'o' are possible centers, and '<' is camera.
		#           # # #
		#         *      #
		#  < o   #    o   #
		#         *      #
		#          # # #
		# As you can see, there are 2 possible centers for this math equation.
		# The answer (real center) is the one that is farther away from the camera,
		# since it implies that the markers are closer than the center (which means
		# that we should be able to see them).
		return cents[0] if distance(cents[0][0], cents[0][1]) > distance(cents[1][0], cents[1][1]) else cents[1]

	# noinspection PySameParameterValue,PyMethodMayBeStatic
	def __get_closest_locations(self, locations, count: int) -> List[Location]:
		"""
		Gets the closest locations out of a list of locations.

		:param locations: The list of locations.
		:param count: The amount of minimums to get (e.g., the 2 closest points)
		:return:
		"""
		# List of points
		minimums: List[Location] = []

		# Convert to a dict like so: {distance: location_object}
		distance_to_point: Dict[float, Location] = {}

		# For each location
		for loc in locations:
			# Get the distance and add it to the dict
			distance_to_point[gbv.plane_distance_from_object(loc)] = loc

		if not distance_to_point:
			raise self.AlgorithmIncomplete()

		# For the amount of minimums to find
		for i in range(count):
			# Get the minimum distance using min(), this will return a key
			# Pop the key's value from the dict
			minimums.append(distance_to_point.pop(min(distance_to_point)))

		return minimums
