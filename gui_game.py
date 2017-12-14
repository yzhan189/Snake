import pygame,sys,time,random

from control.menu_loop import menu_loop
from model.board import Board
from model.snake import Snake
from Button import *
from view.term_draw import draw_surface, show_message
from utils import *
from database import firebase
import io
import requests
from State import *
from Button import *

from AI import AI1,AI12


LEFT = [-1, 0]
RIGHT = [1, 0]
UP = [0, -1]
DOWN = [0, 1]
SCORE_PATH = "./data/score.json"
IMAGE_DIR = "images/"
redColour   = pygame.Color(255,0,0)
blackColour = pygame.Color(0,0,0)
whiteColour = pygame.Color(255,255,255)
greyColour = pygame.Color(200,200,200)
greyColour = pygame.Color(150,150,150)
greenColour = pygame.Color(0,128,0)
yellowColour = pygame.Color(255,255,0)
steelBlue = pygame.Color(70,130,180)

Play_color =  pygame.Color(255,0,0)
player_name = ""
player1_name = ""
player2_name = ""
avatar1_image = None
avatar2_image = None


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
    print(users_by_score)
    # with open(SCORE_PATH, 'r') as f:
    #     score_data = json.load(f)

    back_button = Button()

    while True:
        board_screen.fill((0, 0, 0))
        board_screen.blit(bg, (0, 0))

        back_button.create_button(screen, whiteColour, 30, 100, 100, 50, 60, "Back", steelBlue)


        # the position of the first displaying data (800,520) bottom-left to top-right
        x = 720
        y = 520

        # display avatar, name and score for each player

        for playerName in users_by_score:
            player = users_by_score[playerName]

            # avatar_img = pygame.image.load(player["avatarFilePath"])

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
                    menu_loop()
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
            if event.type == pygame.QUIT:
                quitHelper()
            elif event.type == pygame.MOUSEBUTTONUP:
                if back_button.pressed(pygame.mouse.get_pos()):
                    menu_loop()

#define help center function
def help_loop():
    font = pygame.font.SysFont("arial", 24)
    font_height = font.get_linesize()
    pygame.display.set_caption("Welcome To Snake")
    background = 'data/bg.jpg'
    bg = pygame.image.load(background).convert_alpha()
    back_button = Button()
    while True:
        screen.fill((0, 0, 0))
        screen.blit(bg, (0, 0))
        pygame.draw.polygon(screen, whiteColour, [[175, 225], [175, 400], [900, 400], [900, 225]], 4)
        show_message(screen, 'Press WASD to move snake around!', blackColour, 40, 200, 250)
        show_message(screen, 'move your snake to yellow wormhole to upgrade!', blackColour, 40, 200, 300)
        show_message(screen, 'eat as much food as possible!', blackColour, 40, 200, 350)

        back_button.create_button(screen, whiteColour, 300, 480, 200, 50, 60, "Back", steelBlue)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    menu_loop()
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
            elif event.type == pygame.MOUSEBUTTONUP:
                if back_button.pressed(pygame.mouse.get_pos()):
                    menu_loop()


# define menu loop function
def menu_loop():
    font = pygame.font.SysFont("arial", 24)
    font_height = font.get_linesize()

    pygame.display.set_caption("Welcome To Snake")
    background = 'data/bg.jpg'
    bg = pygame.image.load(background).convert_alpha()

    # 0 for main, 1 for demo choice
    layer = 0
    demo_button = Button()
    play_button = Button()
    leader_button = Button()
    hard_code_AI = Button()
    RL_AI = Button()
    two_AI = Button()
    help_button = Button()
    back_button = Button()
    player_button = Button()
    VS_AI_button = Button()

    # react to input
    while True:
        screen.fill((0, 0, 0))
        screen.blit(bg, (0, 0))

        # main menu
        if layer ==0 :
            play_button.create_button(screen,whiteColour,320,240,200,50,240,"Play",steelBlue)
            demo_button.create_button(screen,whiteColour,320,320,200,50,60,"Demo",steelBlue)
            help_button.create_button(screen,whiteColour,320,400,200,50,60,"Help",steelBlue)
            leader_button.create_button(screen,whiteColour,250,480,400,50,20,"Leader Board",steelBlue)

        # demo
        elif layer == 1:
            hard_code_AI.create_button(screen,whiteColour,300,240,400,50,60,"Hard Coded AI",steelBlue)
            RL_AI.create_button(screen, whiteColour, 300, 320, 400, 50, 60, "Reinforcement Learning AI", steelBlue)
            two_AI.create_button(screen, whiteColour, 300, 400, 400, 50, 60, "Two AI", steelBlue)
            back_button.create_button(screen, whiteColour, 300, 480, 200, 50, 60, "Back", steelBlue)

        # play
        elif layer ==2:
            player_bu1tton.create_button(screen,whiteColour,320,240,200,50,240,"Single Player",steelBlue)
            VS_AI_button.create_button(screen,whiteColour,320,320,200,50,240,"Play with AI",steelBlue)
            back_button.create_button(screen, whiteColour, 320, 400, 200, 50, 60, "Back", steelBlue)



        pygame.display.update()

        # select in menu
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    init_name()
                    standard_mode()
                if event.key == pygame.K_a:   
                    init_name()
                    single_ai_mode()
                if event.key == pygame.K_d:
                    duo_ai_mode()
                if event.key == pygame.K_l:
                    leader_board()
                if event.key == pygame.K_c:
                    clear_data()
                if event.key == pygame.K_h:
                    help_loop()
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONUP:
                if layer ==0:
                    if play_button.pressed(pygame.mouse.get_pos()):
                        layer = 2
                    elif demo_button.pressed(pygame.mouse.get_pos()):
                        layer = 1
                    elif help_button.pressed(pygame.mouse.get_pos()):
                        help_loop()
                    elif leader_button.pressed(pygame.mouse.get_pos()):
                        leader_board()
                elif layer ==1:
                    if hard_code_AI.pressed(pygame.mouse.get_pos()):
                        init_name()
                        single_ai_mode()
                    elif RL_AI.pressed(pygame.mouse.get_pos()):
                        init_name()
                        RL_AI_mode()
                    elif two_AI.pressed(pygame.mouse.get_pos()):
                        duo_ai_mode(True)
                    elif back_button.pressed(pygame.mouse.get_pos()):
                        layer = 0
                elif layer ==2:
                    if player_button.pressed(pygame.mouse.get_pos()):
                        init_name()
                        standard_mode()
                    elif VS_AI_button.pressed(pygame.mouse.get_pos()):
                        duo_ai_mode(False)
                    elif back_button.pressed(pygame.mouse.get_pos()):
                        layer = 0



# define game end
def game_end(total_score, score2 = -1):
    # update total_score
    if score2 == -1:
        updatePlayerData(player_name,total_score)
    else:
        updatePlayerData(player1_name, total_score)
        updatePlayerData(player2_name, score2)
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
            show_message(end_screen, 'Game End', whiteColour, 60, 400, 250)
            show_message(end_screen, 'Press S to come back menu.', blackColour, 40, 250, 350)
            show_message(end_screen, 'Press L to show the leaderBoard.', blackColour, 40, 250, 400)

            if score2 == -1:
                show_message(end_screen, player_name + " you got " + str(total_score) + " points", whiteColour, 30, 250, 450)
            else:
                show_message(end_screen, player1_name + " you got " + str(total_score) + " points", whiteColour, 30, 250, 450)
                show_message(end_screen, player2_name + " you got " + str(score2) + " points", whiteColour, 30, 250, 500)

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        menu_loop()
                    if event.key == pygame.K_l:
                        leader_board()
                if event.type == pygame.QUIT:
                    return
    quitHelper()


def standard_mode():
    # set up local player data
    addPlayerData(player_name)

    screen_size = [700, 700]
    pygame.init()
    fpsClock = pygame.time.Clock()
    playSurface = pygame.display.set_mode((screen_size[0], screen_size[1]))
    my_board = Board(50, 50)
    my_snake = Snake(50, 50)

    # set up food and snake
    food_loc = [my_board.food]
    worm_loc = []
    draw_surface(playSurface, redColour, [my_board.food], 10, 100)  # draw first food
    pygame.display.set_caption('Food Snake')
    total_score = 0
    level = 1
    score = 0
    isEnd = False
    while True:
        # catch event and control snake
        eventHelper(my_snake, True)

        # increase along the moving direction
        draw_surface(playSurface, blackColour, my_snake.get_cells(), 10, 100)
        status = my_snake.tick(my_board.food, my_board.wormhole)

        #if all snake body disappeared, go to next level!
        if my_snake.get_cells() == []:
            my_snake.cells = [[1,1], [1,2], [1,3]] # reassign snake's position!
            level += 1;
            score = 0
            if level == 2:
                for i in range(20, 30, 1):
                    my_snake.obstacles.append([i, 25])
            elif level == 3:
                for i in range(20, 30, 1):
                    my_snake.obstacles.append([i, 15])
                    my_snake.obstacles.append([i, 35])
            worm_loc = []
            my_board.new_food(my_new_cells, my_snake.obstacles, [])
            food_loc = [my_board.food]

        my_snake.teleport_wall()
        my_new_cells = my_snake.get_cells()

        # ending condition
        if my_snake.is_dead([]) or isEnd:
            break
        if status == 1:
            score += my_board.foodWeight
            total_score += 1
            if score > 1:
                my_board.new_wormhole(my_new_cells, my_snake.obstacles, [])
                worm_loc = [my_board.wormhole]
                food_loc = []
            else:
                my_board.new_food(my_new_cells, my_snake.obstacles, [])
                food_loc = [my_board.food]

        # update display each round
        displayHelper(playSurface, fpsClock, level, food_loc, my_snake)


    game_end(total_score)



def RL_AI_mode():
    # q_learning
    # set up local player data
    addPlayerData(player_name)

    # 70*70
    screen_size = [700, 700]
    pygame.init()
    fpsClock = pygame.time.Clock()
    playSurface = pygame.display.set_mode((screen_size[0], screen_size[1]))

    Q = np.genfromtxt('Q100k.csv', delimiter=",")
    print("open file")
    state = State()
    my_board = state.board
    my_snake = state.snake

    # set up food and snake
    food_loc = [my_board.food]
    worm_loc = []
    draw_surface(playSurface, redColour, [my_board.food], 10, 100)  # draw first food
    pygame.display.set_caption('Food Snake')
    total_score = 0
    level = 1
    score = 0
    isEnd = False
    while True:
        # catch event and control snake
        eventHelper(my_snake, False)

        s = state.get_index()

        action = np.argmax(Q[s])
        if action ==0:
            state.turn_right()
        elif action ==2:
            state.turn_left()

        print(my_snake.cells)
        print(food_loc)

        # increase along the moving direction
        draw_surface(playSurface, blackColour, my_snake.get_cells(), 10, 100)
        status = my_snake.tick(my_board.food, None)


        my_snake.teleport_wall()
        my_new_cells = my_snake.get_cells()

        # ending condition
        if my_snake.is_dead([]) or isEnd:
            break
        if status == 1:
            score += my_board.foodWeight
            total_score += 1

            my_board.new_food(my_new_cells, my_snake.obstacles, [])
            food_loc = [my_board.food]

        # update display each round
        displayHelper(playSurface, fpsClock, level, food_loc, my_snake,total_score,player_name,101+state.len*10)


    game_end(total_score)


# this function runs demo mode of one AI
def single_ai_mode():
    # set up local player data
    addPlayerData(player_name)

    screen_size = [700, 700]
    pygame.init()
    fpsClock = pygame.time.Clock()
    # create pyGame screen
    playSurface = pygame.display.set_mode((screen_size[0], screen_size[1]))
    my_board = Board(50, 50)
    my_snake = Snake(50, 50)

    # set up food and snake
    food_loc = [my_board.food]
    draw_surface(playSurface, redColour, [my_board.food], 10, 100)  # draw first food
    pygame.display.set_caption('Food Snake')
    total_score = 0
    score = 0
    level = 1
    isEnd = False

    while True:
        # give AI input, and let AI control snake
        dir = AI1(my_board,my_snake)
        my_snake.turn(dir)

        # catch event and control snake
        eventHelper(my_snake, False)

        # increase along the moving direction
        draw_surface(playSurface, blackColour, my_snake.get_cells(), 10, 100)
        status = my_snake.tick(my_board.food, [])
        my_snake.teleport_wall()
        my_new_cells = my_snake.get_cells()

        if my_snake.is_dead([]) or isEnd:
            break

        # When snake eats the food
        if status == 1:
            score += my_board.foodWeight
            total_score += 1
            my_board.new_food(my_new_cells, my_snake.obstacles, [])
            food_loc = [my_board.food]

            if score - level > level / 2:
                level += 1
            if level % 2 == 0:
                my_snake.add_obstcles(level)
            if level % 3 == 0:
                my_snake.speed += 1

        displayHelper(playSurface, fpsClock, level, food_loc, my_snake,total_score,player_name )


    game_end(total_score)


# define duo mode
def duo_ai_mode(two_AI):
    global player1_name, player2_name, avatar1_image, avatar2_image
    init_name()
    final_score1 = 0
    player1_name = player_name
    avatar1_image = avatar_image
    addPlayerData(player_name)

    # init_name()
    final_score2 = 0
    player2_name = player_name
    avatar2_image = avatar_image
    addPlayerData(player2_name)

    screen_size = [700, 700]
    pygame.init()
    fpsClock = pygame.time.Clock()
    # create pyGame screen
    level = 1
    playSurface = pygame.display.set_mode((screen_size[0], screen_size[1]))
    my_board = Board(50, 50)
    my_snake = Snake(50, 50)
    op_snake = Snake(50, 50)
    op_snake.obstacles = my_snake.obstacles

    # set up food and snake
    food_loc = [my_board.food]
    draw_surface(playSurface, redColour, [my_board.food], 10, 100)  # draw first food
    pygame.display.set_caption('Food Snake')
    total_score = 0
    score = 0
    isEnd = False

    # check input and go as the direction
    while True:
        # give AI input, and let AI control snake
        # o.w human VS AI
        if two_AI:
            dir = AI1(my_board, my_snake)
            my_snake.turn(dir)

        # op is pure AI
        dir = AI12(my_board, op_snake)
        op_snake.turn(dir)

        # catch event and control snake
        eventHelper(my_snake, True)

        # increase along the moving direction
        draw_surface(playSurface, blackColour, my_snake.get_cells(), 10, 100)
        status1 = my_snake.tick(my_board.food, [])
        my_snake.teleport_wall()

        # increase along the moving direction
        draw_surface(playSurface, blackColour, op_snake.get_cells(), 10, 100)
        status2 = op_snake.tick(my_board.food, [])
        op_snake.teleport_wall()

        my_new_cells = my_snake.get_cells()
        op_new_cells = op_snake.get_cells()

        # two player mode
        if my_snake.is_dead(op_new_cells) or op_snake.is_dead(my_new_cells) or isEnd:
            break
        # if AI is dead
        # if op_snake.is_dead(my_new_cells):
        #     score += 10
        #     op_snake = Snake(50, 50)
        #     op_snake.obstacles = my_snake.obstacles

        # When my snake eats the food
        if status1 == 1 or status2 == 1:
            score += my_board.foodWeight
            if status1 == 1:
                final_score1 += 1
            else:
                final_score2 += 1
            my_board.new_food(my_new_cells, my_snake.obstacles, op_new_cells)
            food_loc = [my_board.food]
            if score - level > level / 2:
                level += 1
            if level % 2 == 0:
                my_snake.add_obstcles(level)
            if level % 3 == 0:
                my_snake.speed += 1
        # update display
        displayHelper(playSurface, fpsClock, level, food_loc, my_snake, total_score,player1_name , 601 ,op_new_cells)

    game_end(final_score1)


def init_name():
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
                    return
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


def eventHelper(my_snake,isListenToKey):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quitHelper()

        elif event.type == pygame.KEYDOWN:
            # determine the event of keyBoard
            if (isListenToKey):
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


def displayHelper(playSurface,fpsClock,level,food_loc,my_snake,total_score,player_name ,l = 601,op_new_cells=[]):
    playSurface.fill(blackColour)
    pygame.draw.polygon(playSurface, greenColour, [[99, 99], [99, l], [l, l], [l, 99]], 1)
    show_message(playSurface, 'Score: ' + str(total_score), whiteColour, 40, 10, 10)
    show_message(playSurface, 'Level: ' + str(level), whiteColour, 40, 10, 50)

    screen.blit(avatar_image, (20, 615))
    show_message(playSurface, player_name, whiteColour, 40, 100, 630)

    draw_surface(playSurface, redColour, food_loc, 10, 100)
    draw_surface(playSurface, greenColour, my_snake.obstacles, 10, 100)
    draw_surface(playSurface, whiteColour, my_snake.get_cells(), 10, 100)
    draw_surface(playSurface, greyColour, op_new_cells, 10, 100)

    pygame.display.flip()

    # speed is changeable
    fpsClock.tick(my_snake.speed)


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    total_score = 0
    menu_loop()