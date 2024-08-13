import os
import pygame
pygame.font.init()

WIN_WIDTH = 1400
WIN_HEIGHT = 800

# Rendering Constants
ROCKET_IMGS = [
    pygame.image.load(os.path.join("images", "rocketOff.png")),
    pygame.image.load(os.path.join("images", "rocketOn1.png")),
    pygame.image.load(os.path.join("images", "rocketOn2.png")),
]

STAT_FONT = pygame.font.SysFont("arial", 30)

# Rocket Constants
ROTATION_VEL = 5
ANIMATION_TIME = 3
GRAVITY = 0.3
THRUST = 0.9
MAX_SPEED = 15