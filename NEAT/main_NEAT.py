import sys
from os import path

sys.path.append(path.dirname(path.abspath(__file__)) + "/../")

import pygame
import time
import neat
import pickle
import matplotlib.pyplot as plt
from math import sqrt
from random import randint
from components.constants import (
    ANGLE_CONST,
    BACKGROUND_IMG,
    DISTANCE_CONST,
    FONT_COLOR,
    FPS,
    GEN_NUM,
    GROUND_HEIGHT,
    MAX_GENERATIONS,
    MAX_SPEED,
    MAX_DISTANCE,
    NEARING_TARGET_BONUS,
    OUT_OF_SCREEN_PENALTY,
    RANDOMISE,
    REMAIN_STILL_PENALTY,
    SCENARIO_LENGTH,
    STAT_FONT,
    STAYING_ALIVE_CONST,
    SPAWN_X,
    SPAWN_Y,
    TARGET_X,
    TARGET_IMG,
    TIME_LIMIT,
    TIME_WASTING_PENALTY,
    VELOCITY_CONST,
    WIN_WIDTH,
    WIN_HEIGHT,
    ROCKET_IMGS,
)
from components.rocket import Rocket
from components.base import Ground, Target, Tombstone


def draw_window(win, rockets, base, target, alive, elapsed_time, tombstones):
    win.blit(BACKGROUND_IMG, (0, 0))
    base.draw(win)
    target.draw(win)

    for rocket in rockets:
        rocket.draw(win)

    for tombstone in tombstones:
        tombstone.draw(win)

    generation = STAT_FONT.render(f"Generation: {GEN_NUM}", 1, FONT_COLOR)
    win.blit(generation, (10, 10))

    numAlive = STAT_FONT.render(f"Alive: {alive}", 1, FONT_COLOR)
    win.blit(numAlive, (10, 50))

    fps = STAT_FONT.render(f"FPS: {FPS}", 1, FONT_COLOR)
    win.blit(fps, (10, 90))

    scenario = STAT_FONT.render(
        f"Scene Limit: {SCENARIO_LENGTH} (~{SCENARIO_LENGTH - 1 - (GEN_NUM % SCENARIO_LENGTH)}) [{str(RANDOMISE)[0]}]",
        1,
        FONT_COLOR,
    )
    win.blit(scenario, (10, 130))

    time = STAT_FONT.render(
        f"Time: {round(TIME_LIMIT - elapsed_time, 1)}s", 1, FONT_COLOR
    )
    win.blit(time, (10, 170))

    pygame.display.update()


def main(genomes, config):
    global GEN_NUM, FPS, SPAWN_X, SPAWN_Y, TARGET_X, SCENARIO_LENGTH, RANDOMISE, average_fitness
    GEN_NUM += 1
    if GEN_NUM % SCENARIO_LENGTH == 0:
        TARGET_X = randint(0, WIN_WIDTH - TARGET_IMG.get_width())
        SPAWN_X = randint(0, WIN_WIDTH)
        SPAWN_Y = randint(0, WIN_HEIGHT // 2)
    elif RANDOMISE:
        TARGET_X = randint(
            max(0, TARGET_X - GEN_NUM),
            min(WIN_WIDTH - TARGET_IMG.get_width(), TARGET_X + GEN_NUM),
        )

    rockets = []
    closestDistance = []
    nets = []
    ge = []
    tombstones = []
    totalFitness = 0
    totalPop = 0

    start_time = time.time()

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        # rockets.append(Rocket(SPAWN_X, SPAWN_Y))
        rockets.append(Rocket(randint(0, WIN_WIDTH), randint(0, WIN_HEIGHT // 2)))
        closestDistance.append(MAX_DISTANCE)
        g.fitness = 0
        ge.append(g)
        totalPop += 1

    ground = Ground()
    target = Target(TARGET_X)
    clock = pygame.time.Clock()

    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption(f"Rocket Landing NEAT - Generation {GEN_NUM}")
    pygame.display.set_icon(ROCKET_IMGS[1])

    while True:
        clock.tick(FPS)
        current_time = time.time()
        elapsed_time = current_time - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                best_genome = max(ge, key=lambda g: g.fitness)
                with open("early_stop_winner.pkl", "wb") as f:
                    pickle.dump(best_genome, f)
                plot_fitness()
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            RANDOMISE = not RANDOMISE
        if keys[pygame.K_UP]:
            FPS += 10
        if keys[pygame.K_DOWN]:
            if FPS > 10:
                FPS -= 10
        if keys[pygame.K_i]:
            plot_fitness()
        if keys[pygame.K_RIGHT]:
            SCENARIO_LENGTH += 1
        if keys[pygame.K_LEFT]:
            if SCENARIO_LENGTH > 1:
                SCENARIO_LENGTH -= 1
        if keys[pygame.K_RSHIFT]:
            for x, rocket in enumerate(rockets):
                ge[x].fitness += TIME_WASTING_PENALTY
                if not rocket.changedX:
                    ge[x].fitness += REMAIN_STILL_PENALTY
            break

        for x, rocket in enumerate(rockets):
            rocket.move()
            rocket.calculateDistanceAngle(target)

            ge[x].fitness += STAYING_ALIVE_CONST
            if rocket.distance < closestDistance[x]:
                ge[x].fitness += NEARING_TARGET_BONUS
                closestDistance[x] = rocket.distance

            input_to_NN = (
                rocket.x / WIN_WIDTH,
                rocket.height / (WIN_HEIGHT - GROUND_HEIGHT),
                rocket.angle / 180,
                rocket.velocity_x / MAX_SPEED,
                rocket.velocity_y / MAX_SPEED,
                rocket.distance / MAX_DISTANCE,
                rocket.angle_to_target / 180,
            )

            output = nets[x].activate(input_to_NN)

            if max(output) > 0:
                if output.index(max(output)) == 0:
                    rocket.engagePower()
                elif output.index(max(output)) == 1:
                    rocket.rotateLeft()
                    rocket.disengagePower()
                elif output.index(max(output)) == 2:
                    rocket.rotateRight()
                    rocket.disengagePower()

        for x, rocket in enumerate(rockets):
            if rocket.isLanded():

                if rocket.distance <= 100:
                    ge[x].fitness += 100
                    ge[x].fitness += (WIN_WIDTH - rocket.distance) * DISTANCE_CONST

                    ge[x].fitness += (90 - abs(rocket.angle)) * ANGLE_CONST

                    # ge[x].fitness += (
                    #     sqrt(MAX_SPEED**2 * 2) - rocket.angular_velocity
                    # ) * VELOCITY_CONST
                else:
                    ge[x].fitness -= 100

                if not rocket.changedX:
                    ge[x].fitness += REMAIN_STILL_PENALTY

                tombstones.append(Tombstone(rocket.x, ge[x].fitness))

                totalFitness += ge[x].fitness
                rockets.pop(x)
                closestDistance.pop(x)
                nets.pop(x)
                ge.pop(x)
                continue

            if rocket.isOutOfScreen():
                ge[x].fitness += OUT_OF_SCREEN_PENALTY
                if not rocket.changedX:
                    ge[x].fitness += REMAIN_STILL_PENALTY

                totalFitness += ge[x].fitness
                rockets.pop(x)
                closestDistance.pop(x)
                nets.pop(x)
                ge.pop(x)

        if len(rockets) == 0:
            break

        if elapsed_time > TIME_LIMIT:
            for x, rocket in enumerate(rockets):
                ge[x].fitness += TIME_WASTING_PENALTY
                if not rocket.changedX:
                    ge[x].fitness += REMAIN_STILL_PENALTY
            break

        draw_window(
            win, rockets, ground, target, len(rockets), elapsed_time, tombstones
        )

    average_fitness.append(totalFitness / totalPop)


def plot_fitness():
    plt.clf()
    plt.plot(average_fitness)
    plt.axhline(y=0, color="lightgrey", linestyle="--", linewidth=1)
    plt.xlabel("Generation")
    plt.ylabel("Avg. Fitness")
    plt.title("Average Fitness per Generation")
    plt.savefig(f"avg_fitness.png")
    plt.show(block=False)
    plt.pause(0.01)


def normalise(value, values):
    return (value - min(values) + 1) / (max(values) - min(values) + 1)


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

    with open("best-genome.pkl", "wb") as f:
        pickle.dump(winner, f)

    plot_fitness()

    return winner


if __name__ == "__main__":
    local_dir = path.dirname(__file__)
    config_path = path.join(local_dir, "config-feedforward.txt")
    average_fitness = []
    run(config_path)
