import pygame
import time
import neat
import pickle
from os import path
from math import log, pow
from constants import (
    ANGLE_CONST,
    BACKGROUND_IMG,
    DISTANCE_CONST,
    FONT_COLOR,
    FPS,
    GEN_NUM,
    LANDED_BONUS,
    MAX_GENERATIONS,
    NEARING_TARGET_BONUS,
    OUT_OF_SCREEN_PENALTY,
    REMAIN_STILL_PENALTY,
    STAT_FONT,
    STAYING_ALIVE_BONUS,
    TIME_LIMIT,
    TIME_WASTING_PENALTY,
    VELOCITY_CONST,
    WIN_WIDTH,
    WIN_HEIGHT,
)
from rocket import Rocket
from base import Ground, Target


def draw_window(win, rockets, base, target, alive, elapsed_time):
    win.blit(BACKGROUND_IMG, (0, 0))
    base.draw(win)
    target.draw(win)

    for rocket in rockets:
        rocket.draw(win)

    generation = STAT_FONT.render(f"Generation: {GEN_NUM}", 1, FONT_COLOR)
    win.blit(generation, (10, 10))

    numAlive = STAT_FONT.render(f"Alive: {alive}", 1, FONT_COLOR)
    win.blit(numAlive, (10, 50))

    fps = STAT_FONT.render(f"FPS: {FPS}", 1, FONT_COLOR)
    win.blit(fps, (10, 90))

    time = STAT_FONT.render(
        f"Time: {round(TIME_LIMIT - elapsed_time, 2)}s", 1, FONT_COLOR
    )
    win.blit(time, (10, 130))

    pygame.display.update()


def main(genomes, config):
    global GEN_NUM
    GEN_NUM += 1

    global FPS

    rockets = []
    closestDistance = []
    nets = []
    ge = []

    start_time = time.time()

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        rockets.append(Rocket())
        closestDistance.append(1_000)
        g.fitness = 0
        ge.append(g)

    ground = Ground()
    target = Target()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    while True:
        clock.tick(FPS)
        current_time = time.time()
        elapsed_time = current_time - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            FPS += 10
        if keys[pygame.K_DOWN]:
            if FPS > 10:
                FPS -= 10

        for x, rocket in enumerate(rockets):
            rocket.move()
            rocket.calculateDistance(target)

            ge[x].fitness += STAYING_ALIVE_BONUS
            if rocket.distance < closestDistance[x]:
                ge[x].fitness += NEARING_TARGET_BONUS
                closestDistance[x] = rocket.distance

            input_to_NN = (
                target.center,
                rocket.x,
                rocket.height,
                rocket.angle,
                rocket.velocity_x,
                rocket.velocity_y,
            )

            output = nets[x].activate(input_to_NN)

            if output[0] > 0:
                rocket.engagePower()
            else:
                rocket.disengagePower()

            if output[1] > 0:
                rocket.rotateLeft()

            if output[2] > 0:
                rocket.rotateRight()

        for x, rocket in enumerate(rockets):
            if rocket.isLanded():
                ge[x].fitness += LANDED_BONUS
                ge[x].fitness += (-(log(rocket.distance)) + 2.3) * DISTANCE_CONST
                ge[x].fitness += (
                    -(log(rocket.angular_velocity)) + 0.5
                ) * VELOCITY_CONST
                ge[x].fitness += (1000 - pow(abs(rocket.angle), 1.5)) * ANGLE_CONST

                if not rocket.changedX:
                    ge[x].fitness += REMAIN_STILL_PENALTY

                rockets.pop(x)
                closestDistance.pop(x)
                nets.pop(x)
                ge.pop(x)
                continue

            if rocket.isOutOfScreen():
                ge[x].fitness += OUT_OF_SCREEN_PENALTY

                rockets.pop(x)
                closestDistance.pop(x)
                nets.pop(x)
                ge.pop(x)

        if len(rockets) == 0:
            break

        if elapsed_time > TIME_LIMIT:
            for g in ge:
                g.fitness += TIME_WASTING_PENALTY
            break

        draw_window(win, rockets, ground, target, len(rockets), elapsed_time)

    return


def run(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(main, MAX_GENERATIONS)

    print("\nBest genome:\n{!s}".format(winner))

    with open("winner_genome.pkl", "wb") as f:
        pickle.dump(winner, f)


if __name__ == "__main__":
    local_dir = path.dirname(__file__)
    config_path = path.join(local_dir, "config-feedforward.txt")
    run(config_path)
