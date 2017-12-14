global RIGHT, LEFT, UP, DOWN

LEFT = [-1, 0]
RIGHT = [1, 0]
UP = [0, -1]
DOWN = [0, 1]

def findAvailable(snake):
    directions = [RIGHT, LEFT, UP, DOWN]
    result = []
    for dir in directions:
        if not snake.will_die(dir):
            result.append(dir)
    return result

# this one applies to no other player, no obstacle
def AI1(board,snake):
    availDirections = findAvailable(snake)

    foodX, foodY = board.food
    x, y = snake.cells[-1]
    width = board.width
    height = board.height

    if availDirections ==[]:
        return RIGHT

    # check the "should-go" x direction
    if x == foodX:
        xDir = None
    elif  ( x-foodX>0 and x-foodX<width/2 ) or ( foodX-x>0 and foodX-x>width/2 ):
        xDir = LEFT
    else:
        xDir = RIGHT

    # check y direction
    if y == foodY:
        yDir = None
    elif  ( y-foodY>0 and y-foodY<height/2 ) or ( foodY-y>0 and foodY-y>height/2 ):
        yDir = UP
    else:
        yDir = DOWN

    oldDir = snake.last_direction
    # 3 choices: keep, turn yDir, turn the other yDir
    if oldDir == RIGHT or oldDir == LEFT:
        # no need to turn
        if xDir == oldDir and xDir in availDirections:
            return oldDir
        # you want to fold, first turn to right directoin
        elif yDir is not None and yDir in availDirections:
            return yDir
        elif UP in availDirections:
            return UP
        elif DOWN in availDirections:
            return DOWN
    else:
        if yDir == oldDir and yDir in availDirections:
            return oldDir
        elif xDir is not None and xDir in availDirections:
            return xDir
        elif RIGHT in availDirections:
            return RIGHT
        elif LEFT in availDirections:
            return LEFT

    # catch any exception
    return availDirections[0]

def AI12(board,snake):
    availDirections = findAvailable(snake)

    foodX, foodY = board.food
    x, y = snake.cells[-1]
    width = board.width
    height = board.height

    if availDirections ==[]:
        return RIGHT

    # check the "should-go" x direction
    if x == foodX:
        xDir = None
    elif  ( x-foodX>0 and x-foodX<width/2 ) or ( foodX-x>0 and foodX-x>width/2 ):
        xDir = LEFT
    else:
        xDir = RIGHT

    # check y direction
    if y == foodY:
        yDir = None
    elif  ( y-foodY>0 and y-foodY<height/2 ) or ( foodY-y>0 and foodY-y>height/2 ):
        yDir = UP
    else:
        yDir = DOWN

    oldDir = snake.last_direction
    # 3 choices: keep
    if oldDir == DOWN or oldDir == UP:
        if yDir == oldDir and yDir in availDirections:
            return oldDir
        elif xDir is not None and xDir in availDirections:
            return xDir
        elif RIGHT in availDirections:
            return RIGHT
        elif LEFT in availDirections:
            return LEFT
    else:
        # no need to turn
        if xDir == oldDir and xDir in availDirections:
            return oldDir
        # you want to fold, first turn to right directoin
        elif yDir is not None and yDir in availDirections:
            return yDir
        elif UP in availDirections:
            return UP
        elif DOWN in availDirections:
            return DOWN


    # catch any exception
    return availDirections[0]


