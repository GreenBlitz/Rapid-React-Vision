from cv2 import VideoCapture, FONT_HERSHEY_SIMPLEX
from pupil_apriltags import Detector
import cv2
at_detector = Detector(
families="tag36h11",
   nthreads=1,
   quad_decimate=1.0,
   quad_sigma=0.0,
   refine_edges=1,
   decode_sharpening=0.25,
   debug=0
)
img = cv2.imread("apriltag.jpg")
img1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
image = at_detector.detect(img1)
corners = image[0].corners
center = image[0].center
tag_id = image[0].tag_id
corner_01 = (int(corners[0][0]), int(corners[0][1]))
corner_02 = (int(corners[1][0]), int(corners[1][1]))
corner_03 = (int(corners[2][0]), int(corners[2][1]))
corner_04 = (int(corners[3][0]), int(corners[3][1]))
cv2.line(img, (corner_01[0], corner_01[1]),
                 (corner_02[0], corner_02[1]), (0, 255, 0), 2)
cv2.line(img, (corner_02[0], corner_02[1]),
                 (corner_03[0], corner_03[1]), (0, 255, 0), 2)
cv2.line(img, (corner_03[0], corner_03[1]),
                 (corner_04[0], corner_04[1]), (0, 255, 0), 2)
cv2.line(img, (corner_04[0], corner_04[1]),
                 (corner_01[0], corner_01[1]), (0, 255, 0), 2)
print(image[0])

cv2.putText(img,str(tag_id) , [corner_01[0]+50,corner_01[1]+50], FONT_HERSHEY_SIMPLEX,2,(255,0,0),4)
cv2.imshow("img", img)
cv2.waitKey(0)