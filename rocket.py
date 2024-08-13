from constants import ROCKET_IMGS, ROTATION_VEL, ANIMATION_TIME, GRAVITY, THRUST, MAX_SPEED
from pygame.transform import rotate
from math import cos, sin, radians


class Rocket:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.height = self.y  # unused

        self.tick_count = 0  # unused
        self.velocity_x = 0
        self.velocity_y = 0
        self.power = True

        self.img_count = 0
        self.img = ROCKET_IMGS[0]

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
            center=self.img.get_rect(topleft=(self.x, self.y)).center
        )

        win.blit(rotated_image, new_rect.topleft)

    def move(self):
        # Apply gravity to the vertical velocity
        self.velocity_y += GRAVITY

        if self.power:
            # Adjust thrust components based on the angle (0 degrees is up)
            thrust_x = THRUST * -sin(radians(self.angle))
            thrust_y = THRUST * -cos(radians(self.angle))

            # Update velocity with thrust components
            self.velocity_x += thrust_x
            self.velocity_y += thrust_y

        if self.velocity_x > MAX_SPEED:
            self.velocity_x = MAX_SPEED
        elif self.velocity_x < -MAX_SPEED:
            self.velocity_x = -MAX_SPEED

        if self.velocity_y > MAX_SPEED:
            self.velocity_y = MAX_SPEED
        elif self.velocity_y < -MAX_SPEED:
            self.velocity_y = -MAX_SPEED

        # Update the position of the rocket
        self.x += self.velocity_x
        self.y += self.velocity_y

    def rotateLeft(self):
        self.angle += ROTATION_VEL

    def rotateRight(self):
        self.angle -= ROTATION_VEL

    def engagePower(self):
        self.power = True

    def disengagePower(self):
        self.power = False
