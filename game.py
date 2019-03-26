import sys, pygame

# Variables
# Colors      R    G    B
White =     (255, 255, 255)
Black =     (  0,   0,   0)
Red =       (255,   0,   0)
Green =     (  0, 255,   0)
Blue =      (  0,   0, 255)
Yellowish = (238, 226, 102)
Purple =    (153, 130, 224)
Brown =     (245, 219, 106)
Lightblue = ( 40, 254, 243)


# Game Settings
FPS = 30
fpsClock = pygame.time.Clock()
Display_size = (1000, 1000)
caption = "Hit and Switch"

pygame.init()
Surface = pygame.display.set_mode(Display_size, 0, 32)
pygame.display.set_caption(caption)

# ------------------ No Variables Beyond this line---------------------------------
# Functions


def getfont(text, font, size, color, posx, posy, alignment='center', bold=False, italic=False):
    """ When provided with text, font, size, color, posx, posy and optional alignment, bold, italic options
    Creates a text object at the given position, default as its central alignment, which can be changed if required."""
    textfont = pygame.font.SysFont(font, int(size), bold, italic)
    textbox = textfont.render(text, True, color)
    rect = textbox.get_rect()
    if alignment == 'center':
        rect.center = (posx, posy)
    elif (alignment == 'topright') | (alignment == 'righttop'):
        rect.topright = (posx, posy)
    elif (alignment == 'bottomleft') | (alignment == 'leftbottom'):
        rect.bottomleft = (posx, posy)
    elif (alignment == 'bottomright') | (alignment == 'rightbottom'):
        rect.bottomright = (posx, posy)
    elif (alignment == 'topleft') | (alignment == 'lefttop'):
        rect.topleft = (posx, posy)

    Surface.blit(textbox, rect)
    return rect


def getrect(width, height, posx, posy, color, alignment='center', border=0):
    """ When provided with width, height, x coordinate, y coordinate, color and optional alignment and border options
    creates a rect object with the desired properties and central aligned by default, which can be changed if required"""
    rect = pygame.rect.Rect(posx, posy, width, height)
    if alignment == 'center':
        rect.center = (posx, posy)
    elif (alignment == 'topright') | (alignment == 'righttop'):
        rect.topright = (posx, posy)
    elif (alignment == 'bottomleft') | (alignment =='leftbottom'):
        rect.bottomleft = (posx, posy)
    elif (alignment == 'bottomright') | (alignment == 'rightbottom'):
        rect.bottomright = (posx, posy)
    elif (alignment == 'topleft') | (alignment == 'lefttop'):
        rect.topleft = (posx, posy)

    pygame.draw.rect(Surface, color, rect, border)
    return rect


def getlinesfrom(source):
    """ To get text data from any source file and return as a list of lines"""
    file = open(source)
    data = file.readlines()
    file.close()
    return data


def writelinesto(source, data):
    """ To write the given data to any text file"""
    file = open(source, 'w')
    file.writelines(str(data))
    file.close()


def quitgame():
    """ To quit game"""
    pygame.quit()
    sys.exit()
# ------------------------ No Functions beyond this line ---------------------------------

# Importing Other Files
import start, l1


def main():
    homestat = start.main()
    while homestat == "Go to level 1":
        homestat = l1.main()


if __name__ == "__main__":
    main()
