import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint

from model.board import Board
from model.snake import Snake
from view.term_draw import draw_chr

# UP    = (0, -1)
# DOWN  = (0, 1)
# LEFT  = (-1, 0)
# RIGHT = (1, 0)
LEFT = [0, -1]
RIGHT = [0, 1]
UP = [-1, 0]
DOWN = [1, 0]


curses.initscr()
my_board = Board(20, 60)
my_snake = Snake(20, 60)

win = curses.newwin(my_board.height,my_board.width, 0, 0)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)
key = KEY_RIGHT
score = 0
win.addch(my_board.food[0], my_board.food[1], '*')

while key != 27:  # press Space to exit
    win.border(0)
    win.addstr(0, 2, 'Score : ' + str(score) + ' ')  # Printing 'Score' and
    win.addstr(0, 14, 'Welcome to SNAKE world')  # 'SNAKE' strings
    win.timeout(int(150 - (len(my_snake.cells) / 5 + len(my_snake.cells) / 10) % 120))
    prevKey = key  # Previous key pressed
    event = win.getch()
    key = key if event == -1 else event
    if key == ord(' '):  # If SPACE BAR is pressed, wait for another
        key = -1  # one (Pause/Resume)
        while key != ord(' '):
            key = win.getch()
        key = prevKey
        continue
    if key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:  # If an invalid key is pressed
        key = prevKey
    if key == KEY_LEFT:
        my_snake.turn(LEFT)
    elif key == KEY_RIGHT:
        my_snake.turn(RIGHT)
    elif key == KEY_UP:
        my_snake.turn(UP)
    elif key == KEY_DOWN:
        my_snake.turn(DOWN)

    prev_cells = my_snake.get_cells()
    draw_chr(prev_cells, win, ' ')
    is_eat = my_snake.tick(my_board.food)
    my_snake.teleport_wall()
    if my_snake.is_dead():
        break
    new_cells  = my_snake.get_cells()

    if is_eat:  # When snake eats the food
        score += 1
        my_board.new_food(my_snake.cells)
        draw_chr([my_board.food], win, '*')
    draw_chr(new_cells, win, '#')

curses.endwin()
print("YOUR SCORE:", score)