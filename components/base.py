from components.constants import (
    DEATH_FONT,
    FONT_COLOR,
    GROUND_IMG,
    GROUND_HEIGHT,
    TARGET_IMG,
    TOMBSTONE_IMG,
    WIN_HEIGHT,
)


class Ground:
    def draw(self, win):
        win.blit(GROUND_IMG, (0, WIN_HEIGHT - GROUND_HEIGHT))


class Target:
    def __init__(self, x):
        self.x = x
        self.y = WIN_HEIGHT - GROUND_HEIGHT
        self.center = self.x + TARGET_IMG.get_width() // 2

    def draw(self, win):
        win.blit(TARGET_IMG, (self.x, self.y))


class Tombstone:
    def __init__(self, x, fitness):
        self.x = x
        self.y = WIN_HEIGHT - GROUND_HEIGHT - TOMBSTONE_IMG.get_height()
        self.fitness = str(round(fitness))

    def draw(self, win):
        win.blit(TOMBSTONE_IMG, (self.x, self.y))

        death = DEATH_FONT.render(self.fitness, 1, FONT_COLOR)
        win.blit(death, (self.x, self.y - 10))
