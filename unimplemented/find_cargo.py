"""
Algorithm for locating cargo in the game (red/blue bouncy balls).
"""
from typing import Union, Iterable

import gbrpi
import gbvision as gbv

from algorithms import BaseAlgorithm


class FindCargo(BaseAlgorithm):
	"""
	Cargo finding algorithm.
	"""

	def _process(self, frame: gbv.Frame, camera: gbv.Camera) -> Union[
		gbrpi.ConnEntryValue, Iterable[gbrpi.ConnEntryValue]]:
		pass

	def reset(self, arg):
		pass