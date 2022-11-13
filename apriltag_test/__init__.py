from pupil_apriltags import Detector
import cv2
cam = cv2.VideoCapture(0)
at_detector = Detector(
    families="tag16h5",
    nthreads=1,
    quad_decimate=1.0,
    quad_sigma=0.0,
    refine_edges=1,
    decode_sharpening=0.25,
    debug=0
)




while True:
    ret, img = cam.read()
    img1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    image = at_detector.detect(img1)
    counter = 0
    for i in image:
        corners = image[counter].corners
        center = image[counter].center
        tag_id = image[counter].tag_id
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

        cv2.putText(img, str(tag_id), [corner_01[0] + 50, corner_01[1] + 50], cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0),
                    4)
        counter += 1
    cv2.imshow("img", img)
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break