from random import randint


class Board:

    UP    = ( 0, -1)
    DOWN  = ( 0,  1)
    LEFT  = (-1,  0)
    RIGHT = ( 1,  0)

    def __init__(self,  height, width):
        self.width  = width
        self.height = height
        self.food = [2, 2]

    def new_food(self, cells):
        new_food = [randint(1, self.height-2), randint(1, self.width-2)]
        while new_food in cells:
            new_food = [randint(1, self.height-2), randint(1, self.width-2)]
        self.food = new_food
        return self.food