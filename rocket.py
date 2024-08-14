from constants import (
    ROCKET_IMGS,
    ROTATION_VEL,
    ANIMATION_TIME,
    GRAVITY,
    THRUST,
    MAX_SPEED,
    GROUND_HEIGHT,
    WIN_HEIGHT,
    WIN_WIDTH,
    GROUND_FRICTION,
    BOOSTER_SOUND,
    ANGLE_OFFSET,
)
from pygame.transform import rotate
from math import cos, sin, radians, sqrt


class Rocket:
    def __init__(self, x, y):
        self.img_count = 0
        self.img = ROCKET_IMGS[0]
        self.power = False

        self.x = x
        self.y = y
        self.angle = 0
        self.height = -(
            self.y
            + self.img.get_height()
            - (WIN_HEIGHT - GROUND_HEIGHT)
            - ANGLE_OFFSET[abs(self.angle)]
        )
        self.distance = 0

        self.velocity_x = 0
        self.velocity_y = 0
        self.angular_velocity = 0
        self.last_speed = 0

    def draw(self, win):
        if self.power:
            self.img_count += 1
            if self.img_count < ANIMATION_TIME:
                self.img = ROCKET_IMGS[1]
            elif self.img_count < ANIMATION_TIME * 2 - 1:
                self.img = ROCKET_IMGS[2]
            else:
                self.img_count = 0

        else:
            self.img = ROCKET_IMGS[0]

        rotated_image = rotate(self.img, self.angle)
        new_rect = rotated_image.get_rect(
            center=self.img.get_rect(midtop=(self.x, self.y)).center
        )

        win.blit(rotated_image, new_rect.topleft)

    def move(self):
        self.velocity_y += GRAVITY

        if self.power:
            thrust_x = THRUST * -sin(radians(self.angle))
            thrust_y = THRUST * -cos(radians(self.angle))
            self.velocity_x += thrust_x
            self.velocity_y += thrust_y

        self.velocity_x = max(min(self.velocity_x, MAX_SPEED), -MAX_SPEED)
        self.velocity_y = max(min(self.velocity_y, MAX_SPEED), -MAX_SPEED)
        self.angular_velocity = sqrt(self.velocity_x**2 + self.velocity_y**2)

        self.x += self.velocity_x
        self.y += self.velocity_y

        self.height = -(
            self.y
            + self.img.get_height()
            - (WIN_HEIGHT - GROUND_HEIGHT)
            + ANGLE_OFFSET[abs(self.angle)]
        )
        self.checkCollision()

    def checkCollision(self):
        if self.height <= 0:
            self.y = (
                WIN_HEIGHT
                - GROUND_HEIGHT
                - self.img.get_height()
                - ANGLE_OFFSET[abs(self.angle)]
            )
            self.height = 0
            self.velocity_y = 0
            self.velocity_x *= GROUND_FRICTION
            self.angular_velocity = 0
        else:
            self.last_speed = self.angular_velocity

    def calculateDistance(self, target):
        self.distance = sqrt((self.x - target.center) ** 2 + (self.height) ** 2)

    def normaliseAngle(self):
        if self.angle > 180:
            self.angle -= 360
        elif self.angle < -180:
            self.angle += 360

    def rotateLeft(self):
        self.angle += ROTATION_VEL
        self.normaliseAngle()

    def rotateRight(self):
        self.angle -= ROTATION_VEL
        self.normaliseAngle()

    def engagePower(self):
        if not self.power:
            BOOSTER_SOUND.play(-1, fade_ms=200)
        self.power = True

    def disengagePower(self):
        if self.power:
            BOOSTER_SOUND.stop()
        self.power = False

    def reset(self):
        self.x = WIN_WIDTH // 2
        self.y = 1
        self.angle = 0
        self.height = -(
            self.y
            + self.img.get_height()
            - (WIN_HEIGHT - GROUND_HEIGHT)
            - ANGLE_OFFSET[abs(self.angle)]
        )
        self.distance = 0

        self.velocity_x = 0
        self.velocity_y = 0
        self.angular_velocity = 0
        self.last_speed = 0
        self.power = False
        BOOSTER_SOUND.stop()
        self.img = ROCKET_IMGS[0]
        self.img_count = 0
