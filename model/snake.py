from math import ceil


class Snake:
    LEFT  = [0, -1]
    RIGHT = [0, 1]
    UP    = [-1, 0]
    DOWN  = [1, 0]

    def __init__(self, height, width):
        center = [ceil(height/2), ceil(width/2)]
        self.cells = [center, [center[0], center[1]+1], [center[0], center[1]+2]]
        self.direction = Snake.RIGHT
        self.last_direction = Snake.RIGHT
        self.height = height
        self.width = width

    def is_dead(self):
        if self.cells[0] in self.cells[1:]:
            return True
        else:
            return False

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

    def turn(self, direction):
        if direction == list(map(lambda x: -x, self.last_direction)):
            return False # snake wants to fold over
        self.direction = direction
        return True

    def teleport_wall(self):
        if self.cells[-1][0] == 0:
            self.cells[-1] = [self.height-2, self.cells[-1][1]]

        if self.cells[-1][1] == 0:
            self.cells[-1] = [self.cells[-1][0], self.width-2]

        if self.cells[-1][0] == (self.height-1):
            self.cells[-1] = [1, self.cells[-1][1]]

        if self.cells[-1][1] == (self.width-1):
            self.cells[-1] = [self.cells[-1][0], 1]

    def get_cells(self):
	    return self.cells