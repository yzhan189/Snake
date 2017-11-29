from math import ceil
from unittest import TestCase

from model.snake import Snake


class TestSnake(TestCase):
    def test_is_dead(self):

        my_snake = Snake(20, 60)
        self.assertEquals(my_snake.is_dead(), False)
        center = [ceil(my_snake.height / 2), ceil(my_snake.width / 2)]
        my_snake.cells.append([center[0], center[1]])
        self.assertEquals(my_snake.is_dead(),True)

    def test_tick(self):
        my_snake = Snake(20, 60)
        center = [ceil(my_snake.height / 2), ceil(my_snake.width / 2)]
        food1 = [center[0], center[1] + 3]
        food2 = [center[0], center[1] + 5]
        self.assertEquals(my_snake.tick(food1), True)
        self.assertEquals(my_snake.tick(food2), False)

    def test_turn(self):
        my_snake = Snake(20, 60)
        self.assertEquals(my_snake.turn([-1, 0]), True)
        self.assertEquals(my_snake.turn([0, -1]),  False)

    def test_teleport_wall(self):
        my_snake = Snake(20, 60)
        my_snake.cells = [[0, 30]]
        self.assertEquals(my_snake.teleport_wall(), 0)
        my_snake.cells = [[10, 0]]
        self.assertEquals(my_snake.teleport_wall(), 0)
        my_snake.cells = [[my_snake.height-1, 0]]
        self.assertEquals(my_snake.teleport_wall(), 0)
        my_snake.cells = [[0, my_snake.width-1]]
        self.assertEquals(my_snake.teleport_wall(), 0)

        self.assertEquals(True, True)

    def test_get_cells(self):
        my_snake = Snake(20, 60)
        self.assertEquals(my_snake.cells, my_snake.get_cells())
