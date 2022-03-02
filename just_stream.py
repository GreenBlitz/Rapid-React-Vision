import cv2
import gbvision as gbv
from constants import TCP_STREAM_PORT
front_camera = gbv.USBCamera(0)
tcp_stream = gbv.TCPStreamBroadcaster(TCP_STREAM_PORT)
while True:
    ok, image = front_camera.read()

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
    image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    tcp_stream.send_frame(image)
