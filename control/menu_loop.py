# def menu_loop():  # Menu just for fun
#     pos = 0
#     play_rect = pygame.Rect((SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2), (50, 50))
#     while True:
#         global Play_color
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 exit()
#             elif event.type == MOUSEMOTION:
#                 if play_rect.collidepoint(event.pos):
#                     Play_color = (0, 255, 0)
#                 else:
#                     Play_color = (255, 0, 0)
#             elif event.type == MOUSEBUTTONDOWN:
#                 if play_rect.collidepoint(event.pos):
#                     game_loop()
#             elif event.type == KEYDOWN:
#                 if event.key == K_DOWN or event.key == K_UP:
#                     Play_color = (0, 255, 0)
#                     pos = 1
#                 if event.key == K_RETURN and pos == 1:
#                     game_loop()
#         GameDisplay.fill((0, 0, 0))
#         GameDisplay.blit(bg, (0, 0))
#         play_rect = pygame.draw.rect(GameDisplay, Play_color,
#                                      (Display_Size[0] / 2 - 50, Display_Size[1] / 2 - 25, 100, 50), 0)
#         GameDisplay.blit(font.render("PLAY", True, (0, 0, 0)),
#                          ((Display_Size[0] - font.size("PLAY")[0]) / 2, (Display_Size[1] - font.size("PLAY")[1]) / 2))
#         pygame.display.update()
import pygame


def menu_loop():  # Menu just for fun
    pos = 0
    play_rect = pygame.Rect((600 / 2, 600 / 2), (50, 50))