"""
all game object go in this file
for example:
FUEL = gbv.GameObject(0.01)
"""
import gbvision as gbv
from math import pi

# 136cm diameter hoop
UPPER_HUB_RADIUS = 0.68

# Square root of the circle's area
UPPER_HUB = gbv.GameObject((pi * UPPER_HUB_RADIUS ** 2) ** 0.5)

# 24cm diameter ball
CARGO_BALL = gbv.GameObject((pi * 0.12 ** 2) ** 0.5)
