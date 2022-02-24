"""
Vision master :)
"""
import gbrpi
import gbvision as gbv
from typing import Dict

from algorithms import BaseAlgorithm
from constants import get_stream_port, LED_RING_PORT
from constants import PITCH_ANGLE, YAW_ANGLE, ROLL_ANGLE, X_OFFSET, Y_OFFSET, Z_OFFSET
from constants import generate_camera_ports
from constants import DEV_PORT
from tools import is_on_rpi
from utils import GBLogger

LOGGER_NAME = 'vision_master'
LOG_ALGORITHM_INCOMPLETE = False


# noinspection PyMissingOrEmptyDocstring,PyUnusedFunction
class __EmptyLedRing:
    # noinspection PyUnusedLocal
    def __init__(self, port):
        pass

    def on(self):
        pass

    def off(self):
        pass


LedRing = gbrpi.LedRing if is_on_rpi() else __EmptyLedRing

STREAM = True
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

    # Get the camera ports (mapped out by hardware ports)
    camera_ports = generate_camera_ports()
    front_camera_port = camera_ports["FRONT"]
    # Check my algorithm debug mode
    if STREAM:
        logger.info('running on debug mode, waiting for a stream receiver to connect...')
        front_camera = gbv.USBStreamCamera(gbv.TCPStreamBroadcaster(get_stream_port()), front_camera_port, data=data)
        logger.info('initialized stream')
        front_camera.toggle_stream(True)
    else:
        logger.info('running off debug mode...')
        front_camera = gbv.USBCamera(front_camera_port, data=data)
        front_camera.read()

    # Initialize front_camera settings
    front_camera.set_auto_exposure(False)
    # front_camera.rescale(0.5)  # Makes front_camera frame smaller, if it's being slow or something
    logger.info('initialized front_camera')

    #initializing stream cameras
    back_camera = gbv.USBStreamCamera(get_stream_port(), camera_ports["BACK"], data=data)

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
        #streaming non vision cameras
        back_camera.read()

        ok, frame = front_camera.read()
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
                possible_algos[algo_type].reset(front_camera, led_ring)

            algo = possible_algos[algo_type]
            algo(frame, front_camera)

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
