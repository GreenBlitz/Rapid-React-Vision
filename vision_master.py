"""
Vision master :)
"""
import gbrpi
import gbvision as gbv
from typing import Dict

from algorithms import BaseAlgorithm
from constants import CAMERA_PORT, TCP_STREAM_PORT, LED_RING_PORT
from constants import PITCH_ANGLE, YAW_ANGLE, ROLL_ANGLE, X_OFFSET, Y_OFFSET, Z_OFFSET
from constants import DEV_PORT
from tools import is_on_rpi
from utils import GBLogger

LOGGER_NAME = 'vision_master'
LOG_ALGORITHM_INCOMPLETE = False


# noinspection PyMissingOrEmptyDocstring,PyUnusedFunction
class __EmptyLedRing:
    def __init__(self, port):
        pass

    def on(self):
        pass

    def off(self):
        pass


LedRing = gbrpi.LedRing if is_on_rpi() else __EmptyLedRing


# noinspection PyMissingOrEmptyDocstring
def main():
    # Init gb logger
    logger = GBLogger(LOGGER_NAME, use_file=True)
    logger.allow_debug = BaseAlgorithm.DEBUG

    # START THE CONNECTION. CHANGE THIS TO UART (NETWORK TABLE SUXXXXXX!!)
    conn = gbrpi.UART(DEV_PORT, ["hub"])
    logger.info('initialized conn')

    logger.info('starting conn')
    conn.start_handler_thread()
    logger.info('started conn')

    # Camera and light data
    led_ring = LedRing(LED_RING_PORT)
    data = gbv.LIFECAM_3000.rotate_pitch(PITCH_ANGLE). \
        rotate_yaw(YAW_ANGLE). \
        rotate_roll(ROLL_ANGLE). \
        move_x(X_OFFSET). \
        move_y(Y_OFFSET). \
        move_z(Z_OFFSET)

    if BaseAlgorithm.DEBUG:
        logger.info('running on debug mode, waiting for a stream receiver to connect...')
        camera = gbv.USBStreamCamera(gbv.TCPStreamBroadcaster(TCP_STREAM_PORT), CAMERA_PORT, data=data)
        logger.info('initialized stream')
        camera.toggle_stream(True)
    else:
        logger.info('running off debug mode...')
        camera = gbv.USBCamera(CAMERA_PORT, data=data)

    # Initialize camera settings
    camera.set_auto_exposure(False)
    # camera.rescale(0.5)  # Makes camera frame smaller, if it's being slow or something
    logger.info('initialized camera')

    # Get the algorithms
    all_algos = BaseAlgorithm.get_algorithms()
    logger.debug(f'Algorithms: {", ".join(all_algos)}')
    possible_algos: Dict[str, BaseAlgorithm] = {
        key: all_algos[key](conn, LOG_ALGORITHM_INCOMPLETE) for key in all_algos
    }
    current_algo = None

    # Debugging window
    logger.info('starting debug window if enabled...')
    window = False
    thresh_window = False
    if not BaseAlgorithm.DEBUG and not is_on_rpi():
        # Window setup
        window = gbv.FeedWindow('Vision')
        # Run the window
        window.open()
        # Threshold window setup
        thresh_window = gbv.FeedWindow('Threshold Vision')
        # Run
        thresh_window.open()

    logger.info('starting rpi...')
    while True:
        ok, frame = camera.read()
        # if not is_on_rpi():
        #     algo_type = conn.get('algorithm')
        #     logger.info(f'algo recieved: {algo_type}')
        # else:
        # THIS SHOULD TAKE THE CURRENT ALGORITHM FROM THE NETWORK TABLE
        # (RoboRio chooses an algorithm to use, then waits for result)
        # In the meantime, hardcode only the hub algorithm
        # Since we can't set up the network table atm and we might just make a new lib for it.
        # UPDATE: There is an old UART class we will try to use instead for networking
        algo_type = "hub"

        if algo_type is not None:
            if algo_type not in possible_algos:
                logger.warning(f'Unknown algorithm type: {algo_type}')
            if algo_type != current_algo:
                logger.debug(f'switched to algorithm: {algo_type}')
                possible_algos[algo_type].reset(camera, led_ring)

            algo = possible_algos[algo_type]
            algo(frame, camera)

            if not BaseAlgorithm.DEBUG and window and not is_on_rpi():
                window.show_frame(frame)
            if not BaseAlgorithm.DEBUG and thresh_window and not is_on_rpi():
                # noinspection PyUnresolvedReferences
                shapes = algo.finder.find_shapes(frame)
                thresh_window.show_frame(
                    gbv.draw_rotated_rects(
                        frame=frame,
                        rotated_rects=shapes,
                        color=(255, 0, 0),
                        thickness=1
                    )
                )

        current_algo = algo_type


if __name__ == '__main__':
    main()
