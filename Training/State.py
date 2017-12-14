import numpy as np
from model.snake import Snake
from model.board import Board


# on [0,1]
class State:

    turn = 0

    LEFT = [-1, 0]
    RIGHT = [1, 0]
    UP = [0, -1]
    DOWN = [0, 1]
    # clock-wise
    DIRS = [UP,RIGHT,DOWN,LEFT]

    len = 20
    tile_n = 400

    # snake head * tail * food * direction
    # 400*4*4+1
    total_state_num = tile_n*4 * 4 + 1
    # 3 actions keep, turn right, turn left

    def __init__(self):
        self.snake = Snake(self.len, self.len)
        self.board = Board(self.len, self.len)

    def get_index(self):
        size = self.len
        tile_n = self.tile_n

        self.head_x = self.snake.cells[-1][0]
        self.head_y = self.snake.cells[-1][1]
        self.tail_x = self.snake.cells[0][0]
        self.tail_y = self.snake.cells[0][1]
        self.food_x = self.board.food[0]
        self.food_y = self.board.food[1]

        self.diff_x = self.head_x-self.food_x+size
        self.diff_y = self.head_y-self.food_y+size

        self.ht_x = self.head_x-self.tail_x
        self.ht_y = self.head_y-self.tail_y

        self.dir = self.snake.direction

        if self.snake.is_dead():
            index = self.total_state_num - 1
        else:
            index =  int( self.diff_x + size*2*self.diff_y +\
                        #self.head_x + size*self.head_y + \
                         #tile_n*self.food_x + tile_n*size*self.food_y + \
                        #tile_n*tile_n*self.tail_x + tile_n*tile_n*size*self.tail_y +\
                # self.ht_x*tile_n*4*4 + tile_n*4*4*size * 2 * self.ht_y
                         self.DIRS.index(self.dir)*tile_n*4  )
        return index

    def turn_right(self):
        index = self.DIRS.index(self.dir)
        self.dir = self.DIRS[(index+1)%4]
        self.snake.turn(self.dir)

    def turn_left(self):
        index = self.DIRS.index(self.dir)
        self.dir = self.DIRS[(index - 1) % 4]
        self.snake.turn(self.dir)

    def move_get_rewards(self):
        # return 0 if nothing happen
        # return 1 if got food
        self.snake.teleport_wall()
        reward = self.snake.tick(self.board.food,None)


        if reward == 0:
            reward = - 1 / self.len*2 # negative if in loop
        elif reward == 1:
            self.board.new_food(self.snake.obstacles,[])

        if self.snake.is_dead():
            reward = -1



        return reward





