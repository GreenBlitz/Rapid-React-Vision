from typing import Dict

import gbvision as gbv
import gbrpi

from algorithms import BaseAlgorithm
from constants import CAMERA_PORT, TCP_STREAM_PORT, LED_RING_PORT
from constants import TABLE_IP, TABLE_NAME, OUTPUT_KEY, SUCCESS_KEY
from constants import PITCH_ANGLE, YAW_ANGLE, ROLL_ANGLE, X_OFFSET, Y_OFFSET, Z_OFFSET
from tools import is_on_rpi
from utils import GBLogger

LOGGER_NAME = 'vision_master'
LOG_ALGORITHM_INCOMPLETE = False


class __EmptyLedRing:
    def __init__(self, port):
        pass

    def on(self):
        pass

    def off(self):
        pass


LedRing = gbrpi.LedRing if is_on_rpi() else __EmptyLedRing


def main():
    logger = GBLogger(LOGGER_NAME, use_file=True)
    logger.allow_debug = BaseAlgorithm.DEBUG
    conn = gbrpi.TableConn(ip=TABLE_IP, table_name=TABLE_NAME)
    logger.info('initialized conn')
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
        camera = gbv.USBCamera(CAMERA_PORT, data=data)
    camera.set_auto_exposure(False)
    # camera.rescale(0.5)
    logger.info('initialized camera')

    all_algos = BaseAlgorithm.get_algorithms()

    logger.debug(f'Algorithms: {", ".join(all_algos)}')

    possible_algos: Dict[str, BaseAlgorithm] = {
        key: all_algos[key](OUTPUT_KEY, SUCCESS_KEY, conn, LOG_ALGORITHM_INCOMPLETE) for key in all_algos}
    current_algo = None

    logger.info('starting...')

    while True:
        ok, frame = camera.read()
        algo_type = conn.get('algorithm')
        if algo_type is not None:
            if algo_type not in possible_algos:
                logger.warning(f'Unknown algorithm type: {algo_type}')
            if algo_type != current_algo:
                logger.debug(f'switched to algorithm: {algo_type}')
                possible_algos[algo_type].reset((camera, led_ring))
            algo = possible_algos[algo_type]
            algo(frame, camera)
        current_algo = algo_type


if __name__ == '__main__':
    main()
