"""
all game object go in this file
for example:
FUEL = gbv.GameObject(0.01)
"""
import gbvision as gbv
from math import pi

# 136cm diameter hoop
UPPER_HUB_RADIUS = 0.68

# USE THE REFLECTOR TAPE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! (i spent countless hours trying to debug this...)
# 13cm by 5cm
REFLECTOR_TAPE = gbv.GameObject((0.05 * 0.13) ** 0.5)

# 24cm diameter ball
CARGO_BALL = gbv.GameObject((pi * 0.12 ** 2) ** 0.5)
