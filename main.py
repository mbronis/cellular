import imp
from typing import List
import random
import itertools

import numpy as np

import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN

from src.settings import WIDTH, HEIGHT, TILESIZE, TITLE



class Cave:
    def __init__(self, fill: float = 0.4, seed: int = None) -> None:
        self.fill = fill
        self.seed = seed

        self.map: np.ndarray = self.generate_map()
        self.fill_map_random()
    
    def generate_map(self) -> np.ndarray:
        return np.empty((WIDTH, HEIGHT))

    def fill_map_random(self):
        if self.seed:
            random.seed(self.seed)
        
        for x, y in itertools.product(range(WIDTH), range(HEIGHT)):
            if (x in [0, WIDTH-1]) or (y in [0, HEIGHT-1]):
                self.map[x, y] = 1
                continue
            self.map[x, y] = 1 if random.random() < self.fill else 0
    
    def smooth_map(self):
        pass

    def surrounding_wall_count(self, x, y):
        pass        
        # for x, y in itertools.product(range(WIDTH), range(HEIGHT)):


def draw_cave(screen, cave):
    colors = {
        1: 'brown4',
        0: 'ivory',
    }
    for x, y in itertools.product(range(WIDTH), range(HEIGHT)):
        screen.fill(colors[cave.map[x, y]], get_cell_rect(x, y))

def get_cell_rect(x, y):
    return pygame.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)

def reset_cave(screen):
    cave = Cave()
    draw_cave(screen, cave)
    pygame.display.update()

def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH * TILESIZE, HEIGHT * TILESIZE))
    pygame.display.set_caption(TITLE)

    reset_cave(screen)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == MOUSEBUTTONDOWN:
                reset_cave(screen)

if __name__ == '__main__':
    main()
