"""
all thresholds go in this file
for example:
VISION_TARGET_THRESHOLD = gbv.ColorThreshold([[0, 50], [100, 255], [0, 50]], gbv.ColorThreshold.THRESH_TYPE_BGR)
"""
import gbvision as gbv

UPPER_HUB_THRESHOLD = gbv.ColorThreshold([[55, 75], [255, 256], [110, 255]], 'HSV') + gbv.ErodeAndDilate(4)
