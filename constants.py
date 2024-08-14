import os
from pygame import image, font, mixer

font.init()
mixer.init()

WIN_WIDTH = 1400
WIN_HEIGHT = 800
GROUND_HEIGHT = 50
FPS = 30

# Rendering Constants
ROCKET_IMGS = [
    image.load(os.path.join("images", "rocketOff.png")),
    image.load(os.path.join("images", "rocketOn1.png")),
    image.load(os.path.join("images", "rocketOn2.png")),
]

GROUND_IMG = image.load(os.path.join("images", "ground.png"))
TARGET_IMG = image.load(os.path.join("images", "target.png"))
BACKGROUND_IMG = image.load(os.path.join("images", "background.png"))

BOOSTER_SOUND = mixer.Sound(os.path.join("audio", "booster.mp3"))
BOOSTER_SOUND.set_volume(0.1)

STAT_FONT = font.SysFont("arial", 30)
FONT_COLOR = (0, 0, 0)

# Rocket Constants
ROTATION_VEL = 5
ANIMATION_TIME = 3
GRAVITY = 0.3
THRUST = 0.9
MAX_SPEED = 15
GROUND_FRICTION = 0

ANGLE_OFFSET = {
    0: 0,
    5: 2,
    10: 3,
    15: 4,
    20: 4,
    25: 4,
    30: 4,
    35: 3,
    40: 2,
    45: 0,
    50: -3,
    55: -5,
    60: -7,
    65: -10,
    70: -15,
    75: -18,
    80: -21,
    85: -26,
    90: -30,
    95: -33,
    100: -36,
    105: -34,
    110: -30,
    115: -27,
    120: -23,
    125: -20,
    130: -17,
    135: -15,
    140: -11,
    145: -9,
    150: -6,
    155: -4,
    160: -3,
    165: -1,
    170: 0,
    175: 0,
    180: 0,
}
