import cv2
import gbvision as gbv
import numpy as np
from constants import TCP_STREAM_PORT

thr = gbv.ColorThreshold([[0, 100], [0, 255], [0, 255]])

front_camera = gbv.USBCamera(0)
tcp_stream = gbv.TCPStreamBroadcaster(TCP_STREAM_PORT, max_fps=5)

while True:
	ok, image = front_camera.read()
	# Threshold that bad boy
	ret, mask = cv2.threshold(image[:, :, 2], 150, 255, cv2.THRESH_BINARY)

	# I have literally no clue what this means
	# God speed, stackoverflow.
	mask_color = np.zeros_like(image)
	mask_color[:, :, 0] = mask
	mask_color[:, :, 1] = mask
	mask_color[:, :, 2] = mask

	# Extract the specific color range
	my_color = cv2.bitwise_and(image, mask_color)
	# Extract the rest of the image
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

	# Extract
	gray = cv2.bitwise_and(img, 255 - my_color)

	# orange masked output
	image = image + my_color

	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	width = int(image.shape[1] * 0.2)
	height = int(image.shape[1] * 0.2)
	image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
	image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
	tcp_stream.send_frame(image)
#
# import cv2
# import gbvision as gbv
#
# from constants import TCP_STREAM_PORT
#
# front_camera = gbv.USBCamera(0)
# tcp_stream = gbv.TCPStreamBroadcaster(TCP_STREAM_PORT)
#
# while True:
# 	ok, image = front_camera.read()
#
# 	# R
# 	image[:, :, 2] = image[:, :, 2]
# 	# G
# 	image[:, :, 1] = image[:, :, 1] * 0
# 	# B
# 	image[:, :, 0] = image[:, :, 0] * 0
#
# 	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
# 	width = int(image.shape[1] * 0.2)
# 	height = int(image.shape[1] * 0.2)
# 	image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
# 	image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
# 	tcp_stream.send_frame(image)
