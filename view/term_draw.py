# draw an array of chrs
import pygame
from pygame.rect import Rect


def draw_chr(cells, win, chr):
    # print("---------------")
    # print(cells)
    # print("---------------")
    for cell in cells:
        win.addch(cell[0], cell[1], chr)


def draw_surface(playSurface, color, cells, mult, offset):
    for position in cells:
        posiX = position[0] * 10
        posiY = position[1] * 10
        pygame.draw.rect(playSurface, color, Rect(posiX + offset, posiY + offset, mult, mult))


#display message on screen
def show_message(playSurface, msg, col, size, x=None, y=None):
    fnt = pygame.font.SysFont("SansSerif", size)
    if (x and y) is not None:
        screen_text = fnt.render(msg, True, col)
        playSurface.blit(screen_text, (x, y))
    else:
        screen_text = fnt.render(msg, True, col)
        text_rect = screen_text.get_rect()
        text_rect.center = (700 / 2, 700 / 2)
        playSurface.blit(screen_text, text_rect)