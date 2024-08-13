import pygame
from constants import WIN_WIDTH, WIN_HEIGHT, STAT_FONT
from rocket import Rocket

def draw_window(win, rocket):
    win.fill((255, 255, 255))

    rocket.draw(win)

    text = STAT_FONT.render(
        "Velocity X: " + str(round(rocket.velocity_x, 2)), 1, (0, 0, 0)
    )
    win.blit(text, (10, 10))

    text = STAT_FONT.render(
        "Velocity Y: " + str(round(rocket.velocity_y, 2)), 1, (0, 0, 0)
    )
    win.blit(text, (10, 50))

    pygame.display.update()

def main():
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    rocket = Rocket(300, 300)

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        # Check for key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            rocket.rotateLeft()
        if keys[pygame.K_RIGHT]:
            rocket.rotateRight()
        if keys[pygame.K_SPACE]:
            rocket.engagePower()
        else:
            rocket.disengagePower()

        rocket.move()
        draw_window(win, rocket)

main()
