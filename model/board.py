from random import randint, random

from utils import contains


class Board:

    UP    = ( 0, -1)
    DOWN  = ( 0,  1)
    LEFT  = (-1,  0)
    RIGHT = ( 1,  0)

    def __init__(self,  height, width):
        self.width = width
        self.height = height
        self.food = [10, 10]
        self.wormhole = [1, 1]
        self.foodWeight = 1

    # randomly choose a place to drop the food
    def new_food(self, cells, obstacles, cells_op=[]):
        new_food = [randint(1, self.width-2), randint(1, self.height-2)]
        while new_food in cells or new_food in obstacles or new_food in cells_op:
            new_food = [randint(1, self.width-2), randint(1, self.height-2)]
        self.food = new_food
        return True

    # place a wormhole on the screen, make sure the position is assesible
    def new_wormhole(self, cells, obstacles, cells_op=[]):
        corners = [[1, 1], [1, self.height-2], [self.width-2, 1], [self.width-2, self.height-2]]
        forbiddens = []
        forbiddens.extend(cells)
        forbiddens.extend(obstacles)
        forbiddens.extend(cells_op)

        new_wormhole = [1, 1]
        if contains(forbiddens, corners):
            while new_wormhole in forbiddens:
                new_wormhole = [randint(1, self.width - 2), randint(1, self.height - 2)]
            self.wormhole = new_wormhole
            return new_wormhole
        else:
            while new_wormhole in forbiddens:
                new_wormhole = random.choice(corners)
            self.wormhole = new_wormhole
            return new_wormhole
