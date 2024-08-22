import os
from pygame import image, font, mixer
from random import randint
from math import sqrt

font.init()
mixer.init()

WIN_WIDTH = 1400
WIN_HEIGHT = 800
MAX_DISTANCE = sqrt(WIN_HEIGHT**2 + WIN_WIDTH**2)
GROUND_HEIGHT = 50
FPS = 60

# Rendering Constants
ROCKET_IMGS = [
    image.load(os.path.join("images", "rocketOff.png")),
    image.load(os.path.join("images", "rocketOn1.png")),
    image.load(os.path.join("images", "rocketOn2.png")),
]

GROUND_IMG = image.load(os.path.join("images", "ground.png"))
TARGET_IMG = image.load(os.path.join("images", "target.png"))
BACKGROUND_IMG = image.load(os.path.join("images", "background.png"))
TOMBSTONE_IMG = image.load(os.path.join("images", "tombstone.png"))

BOOSTER_SOUND = mixer.Sound(os.path.join("audio", "booster.mp3"))
BOOSTER_SOUND.set_volume(0.0)

STAT_FONT = font.SysFont("mono", 30)
DEATH_FONT = font.SysFont("arial", 7)
FONT_COLOR = (0, 0, 0)

TARGET_X = randint(0, WIN_WIDTH - TARGET_IMG.get_width())

# Rocket Constants
ROTATION_VEL = 5
ANIMATION_TIME = 3
GRAVITY = 0.1
THRUST = 0.6
MAX_SPEED = 15
GROUND_FRICTION = 0
SPAWN_X = WIN_WIDTH // 2
SPAWN_Y = 10

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

# NEAT Constants
GEN_NUM = 0
MAX_GENERATIONS = 1000
SCENARIO_LENGTH = 1
TIME_LIMIT = 20
RANDOMISE = False

STAYING_ALIVE_CONST = 0.0
NEARING_TARGET_BONUS = 1.0

OUT_OF_SCREEN_PENALTY = -250
TIME_WASTING_PENALTY = -500
REMAIN_STILL_PENALTY = -1_000

DISTANCE_CONST = 0.5
ANGLE_CONST = 2
VELOCITY_CONST = 1
