"""
Base algorithm file.
"""
import abc
import gbrpi
import gbvision as gbv
from typing import Iterable, Dict, Type

from utils.gblogger import GBLogger


class BaseAlgorithm(abc.ABC):
    """
    Base algorithm.
    """
    __registered = {}
    algorithm_name = None
    """
    this is the name of the algorithm, for every algorithm this must be a unique value different from 0
    the network table will tell you which algorithm they currently want to run by using this program
    """
    DEBUG = False
    """
    indicates if the program is being run in debug mode
    not in use by the base program, but should be used by algorithms in order to print extra data in debug mode
    """
    USE_FILE = True

    class AlgorithmIncomplete(BaseException):
        """
        raise this exception when an algorithm cannot complete it's operation successfully and return the wanted result
        for example when a ball-detection algorithm did not find any circles in the frame, so it cannot calculate the
        distance from the closest one
        """

    def __init_subclass__(cls, **kwargs):
        if cls.algorithm_name is None:
            raise AttributeError(f'algorithm_name static field value not set for class {cls.__name__}')
        if cls.algorithm_name in BaseAlgorithm.__registered:
            other_cls = BaseAlgorithm.__registered[cls.algorithm_name]
            raise KeyError(
                f'duplicated entry for algorithm_name {cls.algorithm_name}: {other_cls.__name__} and {cls.__name__}')
        BaseAlgorithm.__registered[cls.algorithm_name] = cls

    def __init__(self, conn: gbrpi.UART, log_algorithm_incomplete=False):
        self.conn = conn
        self.log_algorithm_incomplete = log_algorithm_incomplete
        self.logger = GBLogger(self.algorithm_name, use_file=self.USE_FILE)
        self.logger.allow_debug = self.DEBUG

    def __call__(self, frame: gbv.Frame, camera: gbv.Camera):
        # Holy cow... no comments anywhere... who made this template
        try:
            # Process this frame
            values = self._process(frame, camera)
            # For each value returned from the function
            for value in values:
                # We will send this to the RoboRIO
                self.conn.latest_data = value
            # And send a success message
            self.conn.send_fail()
        except self.AlgorithmIncomplete as e:
            # If something failed
            self.conn.send_fail()
            if self.log_algorithm_incomplete:
                self.logger.warning(repr(e))

    @abc.abstractmethod
    def _process(self, frame: gbv.Frame, camera: gbv.Camera) -> Iterable[gbrpi.ConnEntryValue]:
        """
        processes the frame and returns the result to be placed

        :raises BaseAlgorithm.AlgorithmIncomplete: in case the method cannot return the result
        :param frame: the frame to process
        :param camera: the camera used to capture the frame
        :return: a value, or tuple of values, to put in the network table. a tuple will be provided if the algorithm
            places more than one value in the network table
        """

    @abc.abstractmethod
    def reset(self, camera: gbv.Camera, led_ring: gbrpi.LedRing):
        """
        shamelessly stolen from the Infinite-Recharge-Vision repo, as LedRing will be of use to us once again

        a method that is run every time the current algorithm is switched to this one
        """

    @classmethod
    def get_algorithms(cls) -> Dict[str, Type['BaseAlgorithm']]:
        """
        Return our registered algorithms.
        """
        return cls.__registered.copy()
