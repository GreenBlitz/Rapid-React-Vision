import gbvision as gbv
from constants import PITCH_ANGLE, YAW_ANGLE, ROLL_ANGLE, X_OFFSET, Y_OFFSET, Z_OFFSET, TCP_STREAM_PORT

data = gbv.LIFECAM_3000.rotate_pitch(PITCH_ANGLE). \
    rotate_yaw(YAW_ANGLE). \
    rotate_roll(ROLL_ANGLE). \
    move_x(X_OFFSET). \
    move_y(Y_OFFSET). \
    move_z(Z_OFFSET)

front_camera = gbv.USBStreamCamera(gbv.TCPStreamBroadcaster(TCP_STREAM_PORT), 0, data=data)
front_camera.toggle_stream(True)
