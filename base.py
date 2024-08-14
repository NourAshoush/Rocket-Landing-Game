from constants import (
    GROUND_IMG,
    TARGET_IMG,
    WIN_HEIGHT,
    WIN_WIDTH,
    GROUND_HEIGHT,
    GROUND_FRICTION,
)
from random import randint


class Ground:
    def draw(self, win):
        win.blit(GROUND_IMG, (0, WIN_HEIGHT - GROUND_HEIGHT))


class Target:
    def __init__(self):
        self.x = randint(0, WIN_WIDTH - TARGET_IMG.get_width())
        self.y = WIN_HEIGHT - GROUND_HEIGHT
        self.center = self.x + TARGET_IMG.get_width() // 2

    def draw(self, win):
        win.blit(TARGET_IMG, (self.x, self.y))
