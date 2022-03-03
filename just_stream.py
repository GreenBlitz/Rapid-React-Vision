from threading import Thread

import cv2
import gbvision as gbv
from constants import get_stream_port
from utils.absolute_usb_camera import AbsoluteUSBCamera


def stream(camera, stream):
    while True:
        ok, image = camera.read()

        # R
        image[:, :, 2] = (image[:, :, 2] / 255 * 15) ** 2
        # G
        image[:, :, 1] = image[:, :, 1] / 255 * 70
        # B
        image[:, :, 0] = image[:, :, 0] / 255 * 70

        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        width = int(image.shape[1] * 0.2)
        height = int(image.shape[1] * 0.2)
        image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
        #image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        stream.send_frame(image)


cameras = [AbsoluteUSBCamera("top left"), AbsoluteUSBCamera("bottom left")]
tcp_streams = [gbv.TCPStreamBroadcaster(get_stream_port()), gbv.TCPStreamBroadcaster(get_stream_port())]
while True:
    for i in range(len(cameras)):
        stream(cameras[i], tcp_streams[i])

