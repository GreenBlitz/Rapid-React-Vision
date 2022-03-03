"""
Vision master :)
"""
import gbrpi
import gbvision as gbv
from time import sleep
from typing import Dict, List, Union

from algorithms import BaseAlgorithm
from constants import DEV_PORT, TCP_STREAM_PORT, USB_TO_VIDEO
from constants import LED_RING_PORT
from constants import PITCH_ANGLE, YAW_ANGLE, ROLL_ANGLE, X_OFFSET, Y_OFFSET, Z_OFFSET
from tools import is_on_rpi
from utils import GBLogger
from utils.absolute_usb_camera import AbsoluteUSBCamera

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

    # Check my algorithm debug mode
    cameras: List[Union[AbsoluteUSBCamera, gbv.USBCamera]] = []
    if STREAM:
        logger.info('running on debug mode, waiting for a stream receiver to connect...')
        tcp_stream_conn = gbv.TCPStreamBroadcaster(TCP_STREAM_PORT)
        logger.info('initialized stream')
        logger.info('running cameras...')
        # Open all cameras
        for cam_name in USB_TO_VIDEO:
            # Run camera
            logger.info(f'starting camera "{cam_name}"...')
            # noinspection PyBroadException
            try:
                # Try to open the camera
                camera = AbsoluteUSBCamera(cam_name, data=data)
                logger.info(f'camera "{cam_name}" started!')
                camera.set_auto_exposure(False)
                # camera.rescale(0.5)  # Makes front_camera frame smaller, if it's being slow or something
                # Add to list
                cameras.append(camera)

                # DO NOT TOUCH THIS UNLESS YOU WANT TO SUFFER ETERNAL AGONY, at ur own risk - saji / asaf
                # Free camera variable
                del camera
                # Sleep to prevent camera from boot locking CV2 threads
                sleep(1.5)
            except:
                # If the camera is not active
                logger.info(f'camera "{cam_name}" failed... :(')

        logger.info(f'all active cameras on ({len(cameras)} total)')
    else:
        logger.info('running off debug mode...')
        camera = gbv.USBCamera(conn.cam, data=data)
        camera.read()
        # Put in list
        cameras.append(camera)

    # Get the algorithms
    all_algos = BaseAlgorithm.get_algorithms()
    logger.debug(f'Algorithms: {", ".join(all_algos)}')
    possible_algos: Dict[str, BaseAlgorithm] = {
        key: all_algos[key](conn, LOG_ALGORITHM_INCOMPLETE) for key in all_algos
    }
    current_algo = None

    # Debugging window
    # logger.info('starting debug window if enabled...')
    # window = False
    # thresh_window = False
    # if not BaseAlgorithm.DEBUG and not is_on_rpi():
    #     # Window setup
    #     window = gbv.FeedWindow('Vision')
    #     # Run the window
    #     window.open()
    #     # Threshold window setup
    #     thresh_window = gbv.FeedWindow('Threshold Vision')
    #     # Run
    #     thresh_window.open()

    logger.info('starting rpi...')
    while True:
        ok, frame = cameras[0].read()
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
                possible_algos[algo_type].reset(cameras[0], led_ring)

            algo = possible_algos[algo_type]
            algo(frame, cameras[0])

            # Push to stream
            if STREAM:
                # Get current camera
                ok, frame = cameras[conn.cam].read()
                # Send to stream
                # noinspection PyUnboundLocalVariable
                tcp_stream_conn.send_frame(frame)

            # if not BaseAlgorithm.DEBUG and window and not is_on_rpi():
            #     window.show_frame(frame)
            # if not BaseAlgorithm.DEBUG and thresh_window and not is_on_rpi():
            #     # noinspection PyUnresolvedReferences
            #     shapes = algo.finder.find_shapes(frame)
            #     thresh_window.show_frame(
            #         gbv.draw_rotated_rects(
            #             frame=frame,
            #             rotated_rects=shapes,
            #             color=(255, 0, 0),
            #             thickness=1
            #         )
            #     )

        current_algo = algo_type


if __name__ == '__main__':
    main()
