from math import ceil


class Snake:
    # LEFT  = [0, -1]
    # RIGHT = [0, 1]
    # UP    = [-1, 0]
    # DOWN  = [1, 0]
    LEFT = [-1, 0]
    RIGHT = [1, 0]
    UP = [0, -1]
    DOWN = [0, 1]
    obstacles = []


    def __init__(self, height, width):
        # height and width must be divisible by 10
        center = [ceil(height/2), ceil(width/2)]
        self.cells = [center, [center[0]+1, center[1]], [center[0]+2, center[1]]]
        self.direction = Snake.RIGHT
        self.last_direction = Snake.RIGHT
        self.height = height
        self.width = width
        self.obstacles = []

    # check whether snake is dead or not
    def is_dead(self):
        if self.cells[-1] in self.obstacles:
            return True
        if self.cells[-1] in self.cells[:-1]:
            return True
        else:
            return False

    # go to next frame
    def tick(self, food):
        flag = True  # eat food
        self.cells.append(list(map(lambda x, y: x + y, self.cells[-1], self.direction)))
        self.last_direction = self.direction
        if food != self.cells[-1]:
            self.cells.pop(0)
            flag = False
            return flag
        else:
            return flag

    # turn snake around in specific direction
    def turn(self, direction):
        if direction == list(map(lambda x: -x, self.last_direction)):
            return False # snake wants to fold over
        self.direction = direction
        return True

    # when snake hit the wall, teleport to another side
    def teleport_wall(self):
        if self.cells[-1][0] == 0:
            self.cells[-1] = [self.height-2, self.cells[-1][1]]

        if self.cells[-1][1] == 0:
            self.cells[-1] = [self.cells[-1][0], self.width-2]

        if self.cells[-1][0] == (self.height-1):
            self.cells[-1] = [1, self.cells[-1][1]]

        if self.cells[-1][1] == (self.width-1):
            self.cells[-1] = [self.cells[-1][0], 1]
        return 0


    def get_cells(self):
	    return self.cells