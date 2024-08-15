import pygame
from constants import WIN_WIDTH, WIN_HEIGHT, STAT_FONT, FPS, FONT_COLOR, BACKGROUND_IMG
from rocket import Rocket
from base import Ground, Target


def draw_window(win, rocket, base, target):
    win.blit(BACKGROUND_IMG, (0, 0))

    base.draw(win)
    rocket.draw(win)
    target.draw(win)

    height = STAT_FONT.render(
        "Height: " + str(round(rocket.height, 2)) + "m", 1, FONT_COLOR
    )
    win.blit(height, (WIN_WIDTH - 10 - height.get_width(), 10))

    distance = STAT_FONT.render(
        "Distance: " + str(round(rocket.distance, 2)), 1, FONT_COLOR
    )
    win.blit(distance, (WIN_WIDTH - 10 - distance.get_width(), 50))

    angle = STAT_FONT.render(
        "Angle: " + str(-rocket.angle) + " deg", 1, FONT_COLOR
    )
    win.blit(angle, (WIN_WIDTH - 10 - angle.get_width(), 90))

    vel_x = STAT_FONT.render(
        "Velocity X: " + str(round(rocket.velocity_x, 2)), 1, FONT_COLOR
    )
    win.blit(vel_x, (10, 10))

    vel_y = STAT_FONT.render(
        "Velocity Y: " + str(-round(rocket.velocity_y, 2)), 1, FONT_COLOR
    )
    win.blit(vel_y, (10, 50))

    ang_vel = STAT_FONT.render(
        "Total Velocity: " + str(round(rocket.angular_velocity, 2)), 1, FONT_COLOR
    )
    win.blit(ang_vel, (10, 90))

    pygame.display.update()


def main():
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    rocket = Rocket()
    ground = Ground()
    target = Target()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            rocket.reset()
        if keys[pygame.K_LEFT]:
            rocket.rotateLeft()
        if keys[pygame.K_RIGHT]:
            rocket.rotateRight()
        if keys[pygame.K_SPACE]:
            rocket.engagePower()
        else:
            rocket.disengagePower()

        rocket.move()
        rocket.checkCollision()
        rocket.calculateDistance(target)
        rocket.isLanded()
        rocket.isOutOfScreen()       

        draw_window(win, rocket, ground, target)
        clock.tick(FPS)


main()
