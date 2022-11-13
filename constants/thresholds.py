"""
all thresholds go in this file
for example:
VISION_TARGET_THRESHOLD = gbv.ColorThreshold([[0, 50], [100, 255], [0, 50]], gbv.ColorThreshold.THRESH_TYPE_BGR)
"""
import gbvision as gbv

REFLECTOR_THRESHOLD = gbv.ColorThreshold([[55, 100], [200, 255], [70, 200]], 'HSV') + gbv.ErodeAndDilate(2)
