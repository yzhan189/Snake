from random import randint


class Board:

    UP    = ( 0, -1)
    DOWN  = ( 0,  1)
    LEFT  = (-1,  0)
    RIGHT = ( 1,  0)

    def __init__(self,  height, width):
        self.width = width
        self.height = height
        self.food = [10, 10]
        self.foodWeight = 1

    # randomly choose a place to drop the food
    def new_food(self, cells, obstacles):
        new_food = [randint(1, self.height-2), randint(1, self.width-2)]
        while new_food in cells or new_food in obstacles:
            new_food = [randint(1, self.height-2), randint(1, self.width-2)]
        self.food = new_food
        return True
