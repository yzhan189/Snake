import pygame,sys,time,random
import json
from control.menu_loop import menu_loop
from model.board import Board
from model.snake import Snake
from view.term_draw import draw_surface, show_message
from utils import *

LEFT = [-1, 0]
RIGHT = [1, 0]
UP = [0, -1]
DOWN = [0, 1]
redColour   = pygame.Color(255,0,0)
blackColour = pygame.Color(0,0,0)
whiteColour = pygame.Color(255,255,255)
greyColour = pygame.Color(150,150,150)
greenColour = pygame.Color(0,128,0)
Play_color =  pygame.Color(255,0,0)


player_name = ""
screen = None


WIDTH = 1000
HEIGHT = 600


# define the leaderboard function
def leader_board():
    #to do, display all history score and could redirect back to initial game screen
    pygame.init()
    pygame.mixer.init()
    SCREEN_SIZE = (800, 600)  # This size is for the snake to move around
    Display_Size = (1000, 600)  # this size is for entire screen
    font = pygame.font.SysFont("arial", 24)
    font_height = font.get_linesize()
    board_screen = pygame.display.set_mode(Display_Size, pygame.DOUBLEBUF, 32)
    pygame.display.set_caption("Welcome To Snake")
    background = 'data/bg.jpg'
    bg = pygame.image.load(background).convert_alpha()

    with open(SCORE_PATH, 'r') as f:
        score_data = json.load(f)



    while True:
        board_screen.fill((0, 0, 0))
        board_screen.blit(bg, (0, 0))
        show_message(board_screen, 'Welcome to leaderBoard, press F to return', blackColour, 30, 250, 200)


        x = 100
        y = 240
        for playerName in score_data:
            player = score_data[playerName]
            avatar_img = pygame.image.load(player["avatarFilePath"])
            board_screen.blit(avatar_img, (x, y))
            show_message(board_screen, playerName + ":   "+ str(player["score"]), blackColour, 25, x+60, y+20)
            y += 70
            if (y>HEIGHT-50):
                y = 240
                x += 200

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    init_name()
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

            if event.type == pygame.QUIT:
                quitHelper()








# define menu loop function
def menu_loop():
    Display_Size = (1000, 600)  # this size is for entire screen
    font = pygame.font.SysFont("arial", 24)
    font_height = font.get_linesize()
    #menu_screen = pygame.display.set_mode(Display_Size, pygame.DOUBLEBUF, 32)
    pygame.display.set_caption("Welcome To Snake")
    background = 'data/bg.jpg'
    bg = pygame.image.load(background).convert_alpha()

    # set up local player data
    addPlayerData(player_name)


    while True:
        screen.fill((0, 0, 0))
        screen.blit(bg, (0, 0))
        show_message(screen,'Press S to play or L to show the leaderBoard.', blackColour, 40, 250, 300)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    game_loop(1)
                if event.key == pygame.K_l:
                    leader_board()
            if event.type == pygame.QUIT:
                return




#define game end
def game_end(total_score):

    # update total_score
    updatePlayerData(player_name,total_score)

    while True:
        pygame.init()
        pygame.mixer.init()
        SCREEN_SIZE = (800, 700)  # This size is for the snake to move around
        Display_Size = (1000, 600)  # this size is for entire screen
        font = pygame.font.SysFont("arial", 24)
        font_height = font.get_linesize()
        end_screen = pygame.display.set_mode(Display_Size, pygame.DOUBLEBUF, 32)
        pygame.display.set_caption("Welcome To Snake")
        background = 'data/bg.jpg'
        bg = pygame.image.load(background).convert_alpha()
        while True:
            end_screen.fill((0, 0, 0))
            end_screen.blit(bg, (0, 0))
            show_message(end_screen, 'Game End', blackColour, 40, 250, 300)
            show_message(end_screen, 'Press S to replay or L to show the leaderBoard.', blackColour, 40, 250, 350)
            show_message(end_screen, player_name + " you got " + str(total_score) + " points", blackColour, 40, 250, 400)

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        init_name()
                    if event.key == pygame.K_l:
                        leader_board()
                if event.type == pygame.QUIT:
                    return
    quitHelper()



# define main function
def game_loop(level):
    screen_size = [700, 700]
    game_size   = [500, 500]
    pygame.init()
    fpsClock = pygame.time.Clock()
    # create pyGame screen
    playSurface = pygame.display.set_mode((screen_size[0], screen_size[1]))
    my_board = Board(50, 50)
    my_snake = Snake(50, 50)

    food_loc = [my_board.food]
    draw_surface(playSurface, redColour, [my_board.food], 10, 100) #draw first food
    pygame.display.set_caption('Food Snake')
    total_score = 0
    score = 0
    isEnd = False


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitHelper()

            elif event.type == pygame.KEYDOWN:
                # determine the event of keyBoard
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    my_snake.turn(RIGHT)
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    my_snake.turn(LEFT)
                if event.key == pygame.K_UP or event.key == ord('w'):
                    my_snake.turn(UP)
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    my_snake.turn(DOWN)
                if event.key == ord('q'):
                    isEnd = True
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))


        prev_cells = my_snake.get_cells()
        draw_surface(playSurface, blackColour, prev_cells, 10,  100)
        is_eat = my_snake.tick(my_board.food)
        my_snake.teleport_wall()
        if my_snake.is_dead() or isEnd:
            break
        new_cells = my_snake.get_cells()
        if is_eat:  # When snake eats the food
            score += 1
            total_score += 1
            my_board.new_food(my_snake.cells, my_snake.obstacles)
            food_loc = [my_board.food]

        if score >= 2 and level <= 3:
            level += 1;
            score = 0
            if level == 2:
                for i in range(20, 30, 1):
                    my_snake.obstacles.append([i, 25])
            elif level == 3:
                for i in range(20, 30, 1):
                    my_snake.obstacles.append([i, 15])
                    my_snake.obstacles.append([i, 35])

        playSurface.fill(blackColour)
        pygame.draw.polygon(playSurface, greenColour, [[99, 99], [99, 601], [601, 601], [601, 99]], 1)
        show_message(playSurface, 'Score: '+ str(total_score), whiteColour, 40,  10, 10)
        show_message(playSurface, 'Level: ' + str(level), whiteColour,40,  10, 50)

        screen.blit(avatar_image, (20, 615))
        show_message(playSurface,  player_name, whiteColour, 40, 100, 630)

        draw_surface(playSurface, redColour, food_loc, 10, 100)
        draw_surface(playSurface, greenColour, my_snake.obstacles, 10, 100)


        draw_surface(playSurface, whiteColour, new_cells, 10,  100)
        pygame.display.flip()
        fpsClock.tick(5)

    game_end(total_score)




def init_name():
    # pygame.init()
    # screen = pygame.display.set_mode((1000, 600))
    global player_name

    # default is a random generated name
    name = generateName()

    font = pygame.font.Font(None, 50)
    while True:
        for evt in pygame.event.get():
            if evt.type == pygame.KEYDOWN:
                if evt.unicode.isalpha():
                    name += evt.unicode
                elif evt.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif evt.key == pygame.K_RETURN:
                    # if new name entered, change it
                    if name != '':
                        player_name = name


                    menu_loop()
            elif evt.type == pygame.QUIT:
                return

        # generate avatar, changing according to name entered
        avatar = generateAvatar(name)
        global avatar_image
        avatar_image = pygame.image.load(avatar)

        screen.fill((0, 0, 0))
        show_message(screen, 'Please Enter Your Name: ', whiteColour, 50, 10, 10)

        screen.blit(avatar_image, (WIDTH//2 - 25, HEIGHT//2 + 50))


        block = font.render(name, True, (255, 255, 255))
        rect = block.get_rect()
        rect.center = screen.get_rect().center
        screen.blit(block, rect)
        pygame.display.flip()


def quitHelper():
    pygame.quit()
    setData()
    sys.exit()


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    total_score = 0
    init_name()