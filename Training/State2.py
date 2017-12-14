import numpy as np
from model.snake import Snake
from model.board import Board


# on [0,1]
class State:
    LEFT = [-1, 0]
    RIGHT = [1, 0]
    UP = [0, -1]
    DOWN = [0, 1]
    # clock-wise
    DIRS = [UP,RIGHT,DOWN,LEFT]

    len = 20

    scale = 4
    scale_num = int(len/scale) #5

    tile_n = scale_num*scale_num

    # snake head * tail * food * direction
    # 25*25*16*4+1
    total_state_num = 9 * 9 * 9*9* 4 + 1
    # 3 actions keep, turn right, turn left
    turn = 0

    def __init__(self):
        self.snake = Snake(self.len, self.len)
        self.board = Board(self.len, self.len)

    def get_index(self):

        tile_n = self.tile_n
        scale_num = self.scale_num
        scale = self.scale
        # 0 - 19
        # 0,1,2,3,4
        self.head_x = self.snake.cells[-1][0] // 4
        self.head_y = self.snake.cells[-1][1] // 4
        self.tail_x = self.snake.cells[0][0] // 4
        self.tail_y = self.snake.cells[0][1] // 4
        self.food_x = self.board.food[0] // 4
        self.food_y = self.board.food[1] // 4

        # -4321, 0 , 1234
        self.diff_x = int( self.head_x-self.food_x + 4  )
        self.diff_y = int( self.head_y-self.food_y +4  )

        self.ht_x = int( self.head_x-self.tail_x+4 )
        self.ht_y = int( self.head_y-self.tail_y+4 )

        size = scale_num*2

        self.dir = self.snake.direction

        if self.snake.is_dead():
            index = self.total_state_num - 1
        else:
            index =  int( self.diff_x + 9*self.diff_y +\
                            self.ht_x*9*9+ self.ht_y*9*9*9 +\
                        #self.head_x + size*self.head_y + \
                         #tile_n*self.food_x + tile_n*size*self.food_y + \
                        #tile_n*tile_n*self.tail_x + tile_n*tile_n*size*self.tail_y +\
                         self.DIRS.index(self.dir)*9*9*9*9 )
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
        self.turn+=1
        self.snake.teleport_wall()
        reward = self.snake.tick(self.board.food,None)


        if reward == 0:
            reward = - 1 / (self.len * 2) # negative if in loop
        elif reward == 1:
            self.board.new_food(self.snake.obstacles,[])

        if self.snake.is_dead() :
            reward = -1



        return reward





