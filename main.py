import curses
from curses import textpad
from copy import deepcopy
import random


def gen_dead_world(height, width):
    world = [[" " for _ in range(width)] for _ in range(height)]
    return world


def gen_random_world(height, width):
    empty_world = gen_dead_world(height, width)
    for y, row in enumerate(empty_world):
        for x, _ in enumerate(row):
            if random.random() < 0.5:
                empty_world[y][x] = "*"
            else:
                empty_world[y][x] = " "
    return empty_world


def gen_glider(world, y, x):
    world[y - 1][x] = "*"
    world[y][x + 1] = "*"
    world[y + 1][x - 1] = "*"
    world[y + 1][x] = "*"
    world[y + 1][x + 1] = "*"


def neighbors_count(world, y, x):
    total_alive = 0
    for adjy, adjx in neighbors_gen(world, y, x):
        if world[adjy][adjx] == "*":

            total_alive += 1
    return total_alive


def neighbors_gen(world, y, x):

    maxw = len(world[0])
    maxh = len(world)
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            adjy = y + dy
            adjx = x + dx
            if (y, x) != (adjy, adjx):

                if y + dy == maxh:
                    adjy = 0

                if y + dy < 0:
                    adjy = maxh - 1

                if x + dx == maxw:
                    adjx = 0

                if x + dx < 0:
                    adjx = maxw - 1

                yield adjy, adjx


def next_world_state(world):
    new_world = deepcopy(world)
    for y, row in enumerate(world):
        for x, _ in enumerate(row):
            new_world[y][x] = decide_fate(world, y, x)
    return new_world


def decide_fate(world, y, x):
    neighbors = neighbors_count(world, y, x)

    state = world[y][x]

    if state == "*":
        if neighbors in [2, 3]:
            new_fate = "*"
        else:
            new_fate = " "
    else:
        if neighbors == 3:
            new_fate = "*"
        else:
            new_fate = " "
    return new_fate


def draw_world(win, world):
    for y, row in enumerate(world):
        for x, being in enumerate(row):
            win.addstr(y, x, being)


def editor_main(stdscr):
    timemax = 1000
    world = gen_random_world(curses.LINES - 1, curses.COLS - 1)
    for _ in range(timemax):
        draw_world(stdscr, world)
        world = next_world_state(world)
        stdscr.refresh()


curses.wrapper(editor_main)
