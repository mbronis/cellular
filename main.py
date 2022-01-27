import imp
from typing import List
import random
import itertools

import numpy as np

import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN


TITLE = 'A cellular automata game'
FPS = 10

WIDTH = 120
HEIGHT = 60
TILESIZE = 10

FILL = 0.4


class Cave:
    def __init__(self, fill: float = FILL, seed: int = None) -> None:
        self.fill = fill
        self.seed = seed

        self.map = self.generate_map()
        self.rect = self.generate_map_rect()
        self.fill_map_random()
    
    def generate_map(self) -> np.ndarray:
        return np.empty((WIDTH, HEIGHT))

    def generate_map_rect(self):
        rect = dict()
        for x, y in itertools.product(range(WIDTH), range(HEIGHT)):
            rect[(x, y)] = get_cell_rect(x, y)
        
        return rect

    def fill_map_random(self):
        if self.seed:
            random.seed(self.seed)
        
        for x, y in itertools.product(range(WIDTH), range(HEIGHT)):
            if (x in [0, WIDTH-1]) or (y in [0, HEIGHT-1]):
                self.map[x, y] = 1
                continue
            self.map[x, y] = 1 if random.random() < self.fill else 0
    
    def smooth_map(self):
        for x, y in itertools.product(range(WIDTH), range(HEIGHT)):
            if (x == 0) or (x == WIDTH-1) or (y == 0) or (y == HEIGHT-1):
                continue

            walls_count = self.surrounding_wall_count(x, y)
            if walls_count > 4:
                self.map[x, y] = 1
            elif walls_count < 4:
                self.map[x, y] = 0

    def surrounding_wall_count(self, x, y):
        walls_count = 0
        for nx, ny in itertools.product(range(x-1, x+2), range(y-1, y+2)):
            if (nx < 0) or (nx > WIDTH-1) or (ny < 0) or (ny > HEIGHT-1):
                continue
            walls_count += self.map[nx, ny]
        
        return walls_count

def draw_cave(screen, cave):
    colors = {
        1: 'brown4',
        0: 'ivory',
    }
    for x, y in itertools.product(range(WIDTH), range(HEIGHT)):
        screen.fill(colors[cave.map[x, y]], cave.rect[(x, y)])

def get_cell_rect(x, y):
    return pygame.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)

def reset_cave(screen):
    cave = Cave()
    draw_cave(screen, cave)
    pygame.display.update()

    return cave

def smooth_cave(screen, cave):
    cave.smooth_map()
    draw_cave(screen, cave)
    pygame.display.update()

def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH * TILESIZE, HEIGHT * TILESIZE))
    pygame.display.set_caption(TITLE)
    
    clock = pygame.time.Clock()

    cave = reset_cave(screen)
    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == MOUSEBUTTONDOWN:
                cave = reset_cave(screen)

        smooth_cave(screen, cave)

if __name__ == '__main__':
    main()
