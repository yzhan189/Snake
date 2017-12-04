import pygame,sys,time,random

from control.menu_loop import menu_loop
from model.board import Board
from model.snake import Snake
from view.term_draw import draw_surface, show_message
from utils import *
from database import firebase
import io
import requests

from AI import AI1,AI12


LEFT = [-1, 0]
RIGHT = [1, 0]
UP = [0, -1]
DOWN = [0, 1]
redColour   = pygame.Color(255,0,0)
blackColour = pygame.Color(0,0,0)
whiteColour = pygame.Color(255,255,255)
greyColour = pygame.Color(200,200,200)
greyColour = pygame.Color(150,150,150)
greenColour = pygame.Color(0,128,0)
Play_color =  pygame.Color(255,0,0)


player_name = ""
screen = None


WIDTH = 1000
HEIGHT = 600
Display_Size = (1000, 600)  # this size is for entire screen


# leaderboard
def leader_board():
    # set the data, before displaying
    setData()

    pygame.init()
    pygame.mixer.init()
    font = pygame.font.SysFont("arial", 24)
    font_height = font.get_linesize()
    board_screen = pygame.display.set_mode(Display_Size, pygame.DOUBLEBUF, 32)
    pygame.display.set_caption("Welcome To Snake")
    background = 'data/bg.jpg'
    bg = pygame.image.load(background).convert_alpha()

    # load firebase
    db = firebase.database()
    storage = firebase.storage()
    # display the top 20 players with highest scores
    users_by_score = db.child("players").order_by_child("score").limit_to_last(20).get().val()

    while True:
        board_screen.fill((0, 0, 0))
        board_screen.blit(bg, (0, 0))
        show_message(board_screen, 'Welcome to leaderBoard, press F to return', blackColour, 30, 250, 200)

        # the position of the first displaying data
        x = 750
        y = 520

        # display avatar, name and score for each player

        for playerName in users_by_score:
            player = users_by_score[playerName]

            image_url = storage.child(player["avatarFilePath"]).get_url(None)

            response = requests.get(image_url)
            image_file = io.BytesIO(response.content)
            avatar_img = pygame.image.load(image_file)

            board_screen.blit(avatar_img, (x, y))

            show_message(board_screen, playerName + ":   "+ str(player["score"]), blackColour, 25, x+60, y+20)
            y -= 70
            if (y<240):
                y = 520
                x -= 220

        # check input
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
    font = pygame.font.SysFont("arial", 24)
    font_height = font.get_linesize()

    pygame.display.set_caption("Welcome To Snake")
    background = 'data/bg.jpg'
    bg = pygame.image.load(background).convert_alpha()

    # set up local player data
    addPlayerData(player_name)

    # react to input
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

    # display ending message
    while True:
        pygame.init()
        pygame.mixer.init()
        font = pygame.font.SysFont("arial", 24)
        font_height = font.get_linesize()
        end_screen = pygame.display.set_mode(Display_Size, pygame.DOUBLEBUF, 32)
        pygame.display.set_caption("Welcome To Snake")
        background = 'data/bg.jpg'
        bg = pygame.image.load(background).convert_alpha()

        # check input
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
    op_snake = Snake(50, 50)
    op_snake.obstacles = my_snake.obstacles

    # set up food and snake
    food_loc = [my_board.food]
    draw_surface(playSurface, redColour, [my_board.food], 10, 100) #draw first food
    pygame.display.set_caption('Food Snake')
    total_score = 0
    score = 0
    isEnd = False


    # check input and go as the direction
    while True:
        # give AI input, and let AI control snake
        dir = AI1(my_board,my_snake)
        my_snake.turn(dir)

        # op is pure AI
        dir = AI12(my_board,op_snake)
        op_snake.turn(dir)

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

        # increase along the moving direction
        draw_surface(playSurface, blackColour, my_snake.get_cells(), 10,  100)
        is_eat = my_snake.tick(my_board.food)
        my_snake.teleport_wall()

        # increase along the moving direction
        draw_surface(playSurface, blackColour, op_snake.get_cells(), 10,  100)
        is_eat_op = op_snake.tick(my_board.food)
        op_snake.teleport_wall()


        my_new_cells = my_snake.get_cells()
        op_new_cells = op_snake.get_cells()

        if my_snake.is_dead(op_new_cells) or op_snake.is_dead(my_new_cells) or isEnd:
            break

        # When snake eats the food
        if is_eat:
            score += my_board.foodWeight
            total_score += 1
            my_board.new_food(my_new_cells, my_snake.obstacles, op_new_cells)

        if is_eat or is_eat_op:
            food_loc = [my_board.food]

            if score-level > level/2:
                level += 1

            if level%2 == 0:
                my_snake.add_obstcles(level)
            if level%3 == 0:
                my_snake.speed += 1


        playSurface.fill(blackColour)
        pygame.draw.polygon(playSurface, greenColour, [[99, 99], [99, 601], [601, 601], [601, 99]], 1)
        show_message(playSurface, 'Score: '+ str(total_score), whiteColour, 40,  10, 10)
        show_message(playSurface, 'Level: ' + str(level), whiteColour,40,  10, 50)

        screen.blit(avatar_image, (20, 615))
        show_message(playSurface,  player_name, whiteColour, 40, 100, 630)

        draw_surface(playSurface, redColour, food_loc, 10, 100)
        draw_surface(playSurface, greenColour, my_snake.obstacles, 10, 100)


        draw_surface(playSurface, whiteColour, my_new_cells, 10,  100)
        draw_surface(playSurface, greyColour, op_new_cells, 10,  100)

        pygame.display.flip()

        # speed is changeable
        fpsClock.tick(my_snake.speed)


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

# quit, clean up all local data
def quitHelper():
    pygame.quit()
    # set data every time you quit
    setData()
    sys.exit()


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    total_score = 0
    init_name()