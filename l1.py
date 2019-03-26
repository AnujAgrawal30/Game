from game import *
import random, math
from pygame.locals import *


def main():
    global star, diamond, speed, score, lives, toggle, heart, lose_game, high_score     # Global variables
    """ Getting assets ready """
    high_score = getlinesfrom('high_score.txt')
    star = pygame.image.load("star.png")
    heart = pygame.image.load('heart.png')
    diamond = pygame.image.load("diamond.png")
    """Game Settings for the particular level """
    initial_speed = 4                           # Initial speed of the objects
    speed = initial_speed                       # Speed during gameplay
    lives = 3
    heart_count = 1                             # To give extra lives at regular score intervals
    score = 0
    initial_freq = 0.2                          # Initial frequency of the object's appearance
    freq = initial_freq                         # Frequency during gameplay
    counter = 0                                 # To count till next entry of new object
    box_data = [[], [], [], [], [], [], [], []] # To keep track of Objects on all 8 tracks
    gamestate = [True, True, True, True]        # To keep track of positions of the 4 pairs of tracks
    toggle = True                               # To track the functional direction of tracks (Top-left or Bottom-right)
    lose_game = False                           # To ensure once lost the Game Ends

    """ Assets Properties """
    TextColor = Black

    while True:  # Main Game Loop
        if lose_game:
            """ If Game is lost the game stops and waits for user input to either restart the Game or quit"""
            while True:
                pygame.display.update()
                center_rect = getrect(500, 400, Display_size[0]/2, Display_size[1]/2, Red)
                if score > int(high_score[0]):
                    getfont(str('New High Score: ' + str(score)), 'bahnchrift', 50, TextColor, center_rect.midtop[0],
                            center_rect.top + 50)
                    writelinesto('high_score.txt', score)
                else:
                    getfont(str('Your Score: ' + str(score)), 'bahnchrift', 50, TextColor, center_rect.midtop[0],
                            center_rect.top + 50)
                replay_rect = getrect(300, 50, center_rect.midtop[0], center_rect.top + 200, White)
                getfont('Replay', 'bahnchrift', 50, TextColor, replay_rect.center[0], replay_rect.center[1])
                quit_rect = getrect(300, 50, center_rect.midtop[0], center_rect.top + 300, White)
                getfont('Quit', 'bahnchrift', 50, TextColor, quit_rect.center[0], quit_rect.center[1])
                for event in pygame.event.get():
                    if event.type == QUIT:
                        quitgame()
                    if event.type == MOUSEBUTTONDOWN:
                        if replay_rect.collidepoint(event.pos):
                            return "Go to level 1"
                        elif quit_rect.collidepoint(event.pos):
                            quitgame()
        """ If Game not lost, continue with the Gameplay """
        drawSurface(gamestate, box_data)
        for event in pygame.event.get():
            if event.type == QUIT:
                quitgame()
            elif event.type == KEYDOWN:
                if (event.key == K_UP) | (event.key == K_w):
                    if toggle:
                        gamestate[0] = True
                    else:
                        gamestate[2] = False
                elif (event.key == K_DOWN) | (event.key == K_s):
                    if toggle:
                        gamestate[0] = False
                    else:
                        gamestate[2] = True
                elif (event.key == K_LEFT) | (event.key == K_a):
                    if toggle:
                        gamestate[1] = False
                    else:
                        gamestate[3] = True
                elif (event.key == K_RIGHT) | (event.key == K_d):
                    if toggle:
                        gamestate[1] = True
                    else:
                        gamestate[3] = False
                elif event.key == K_SPACE:
                    toggle = not toggle
        fpsClock.tick(FPS)
        counter += 1
        if counter > int(FPS/freq):
            i = random.randint(0, 7)
            j = random.randint(0, 1)
            if score/500 > heart_count:
                box_data[i].append([heart, 0])
                heart_count += 1
                i = 7-i
            if j == 0:
                box_data[i].append([star, 0])
            else:
                box_data[i].append([diamond, 0])
            counter = 0
        if score >= 0:
            speed = initial_speed*(math.log(score/1000 + 1) + 1)
            freq = initial_freq*(math.log(score/100 + 1) + 1)


def drawSurface(gamestate, box_data):

    def check_end(obj, box):
        """ Checks if the object has reached its end of the bar, and if yes removes the object from the list and
        performs necessary action according to the final position of the object """
        global lives, lose_game, score
        if obj[1] > bar_length:  # If the sprite has reached its length, check for its status and then delete it
            if (obj[0] == star) & ((rect.center[0] == center_rect.center[0]) | (rect.center[1] == center_rect.center[1])):
                lives -= 1
                if lives == 0:
                    lose_game = True
            elif obj[0] == diamond:
                if (rect.center[0] == center_rect.center[0]) | (rect.center[1] == center_rect.center[1]):
                    score += 100
                else:
                    score -= 100
                    if score < 0:
                        lose_game = True
            elif obj[0] == heart:
                if (rect.center[0] == center_rect.center[0]) | (rect.center[1] == center_rect.center[1]):
                    if lives < 5:
                        lives += 1
            del box_data[box][0]


    global score, lives, lose_game, high_score

    """ Assets properties """
    bar_length = Display_size[0]*0.4
    bar_width = bar_length/8
    BGcolor = Blue
    TextColor = Black
    button_color = Yellowish
    button_color2 = Red
    border_color = Green
    inner_boxcolor = Brown
    border = 5

    """ Displaying Game State """
    Surface.fill(BGcolor)
    getfont(caption, 'bahnchrift', 50, TextColor, Display_size[0]/4, Display_size[1]/12, italic=True)
    textbox = getfont(str("Score: " + str(score)), 'bahnchrift', 50, TextColor, Display_size[0]*3/4, Display_size[1]/12,
                      italic=True)
    textbox = getfont(str("Lives: " + str(lives)), 'bahnchrift', 50, TextColor, textbox.bottomleft[0],
                      textbox.bottomleft[1], alignment='topleft',  italic=True)
    getfont(str("High Score: " + str(int(high_score[0]))), 'bahnchrift', 50, TextColor, textbox.bottomleft[0],
            textbox.bottomleft[1], alignment='topleft',  italic=True)

    """ Creating Central Boxes """
    center_rect = pygame.rect.Rect(0, 0, 3*bar_width, 3*bar_width)
    center_rect.center = (Display_size[0]/2, Display_size[1]/2)
    getrect(3*bar_width, bar_width, Display_size[0] / 2, Display_size[1] / 2, inner_boxcolor)
    getrect(bar_width, 3*bar_width, Display_size[0] / 2, Display_size[1] / 2, inner_boxcolor)
    getrect(bar_width, bar_width, Display_size[0] / 2, Display_size[1] / 2, Black, border=border)
    rect = pygame.rect.Rect(center_rect[0], center_rect[1], bar_length, bar_width)

    """ gamestat[i] means to check if the left(i = 0), right(i = 2), top(i = 1), or bottom(i = 3) is in its initial
    position or not."""
    """Drawing and simulating Left Rectangle """
    rect.midright = center_rect.midleft

    if gamestate[0]:
        """ Creating lower box """
        pygame.draw.rect(Surface, button_color2, rect)
        for obj in box_data[0]:
            Surface.blit(obj[0], (rect.topleft[0] + obj[1], rect.topleft[1]))
            obj[1] += speed
            check_end(obj, 0)
        """ Creating upper box"""
        rect.bottom = rect.top
        pygame.draw.rect(Surface, button_color, rect)
        pygame.draw.line(Surface, Black, rect.bottomleft, rect.bottomright)
        for obj in box_data[1]:
            Surface.blit(obj[0], (rect.topleft[0] + obj[1], rect.topleft[1]))
            obj[1] += speed
            check_end(obj, 1)
    else:
        """ Creating upper box """
        pygame.draw.rect(Surface, button_color, rect)
        for obj in box_data[1]:
            Surface.blit(obj[0], (rect.topleft[0] + obj[1], rect.topleft[1]))
            obj[1] += speed
            check_end(obj, 1)
        """ Creating lower box """
        rect.top = rect.bottom
        pygame.draw.rect(Surface, button_color2, rect)
        for obj in box_data[0]:
            Surface.blit(obj[0], (rect.topleft[0] + obj[1], rect.topleft[1]))
            obj[1] += speed
            check_end(obj, 0)
        pygame.draw.line(Surface, Black, rect.topleft, rect.topright)
    """ Drawing boundary if toggle is active"""
    if toggle:
        getrect(bar_length, 3*bar_width, center_rect.topleft[0], center_rect.topleft[1], Lightblue, border=border,
                alignment='topright')

    """ Drawing and simulating Right Rectangle """
    rect.midleft = center_rect.midright
    if gamestate[2]:
        """ Creating upper box """
        pygame.draw.rect(Surface, button_color2, rect)
        for obj in box_data[4]:
            Surface.blit(obj[0], (rect.bottomright[0] - bar_width - obj[1], rect.bottomright[1] - bar_width))
            obj[1] += speed
            check_end(obj, 4)
        """ Creating lower box """
        rect.top = rect.bottom
        pygame.draw.rect(Surface, button_color, rect)
        for obj in box_data[5]:
            Surface.blit(obj[0], (rect.bottomright[0] - bar_width - obj[1], rect.bottomright[1] - bar_width))
            obj[1] += speed
            check_end(obj, 5)
    else:
        """ Creating lower box """
        pygame.draw.rect(Surface, button_color, rect)
        for obj in box_data[5]:
            Surface.blit(obj[0], (rect.bottomright[0] - bar_width - obj[1], rect.bottomright[1] - bar_width))
            obj[1] += speed
            check_end(obj, 5)
        """Creating upper box """
        rect.bottom = rect.top
        pygame.draw.rect(Surface, button_color2, rect)
        for obj in box_data[4]:
            Surface.blit(obj[0], (rect.bottomright[0] - bar_width - obj[1], rect.bottomright[1] - bar_width))
            obj[1] += speed
            check_end(obj, 4)

    """ Drawing boundary if toggle is inactive """
    if not toggle:
        getrect(bar_length, 3*bar_width, center_rect.topright[0], center_rect.topright[1], Lightblue, border=border,
                alignment='topleft')
    rect = pygame.rect.Rect(center_rect[0], center_rect[1], bar_width, bar_length)

    """ Drawing and simulating Top Rectangle """
    rect.midbottom = center_rect.midtop
    if gamestate[1]:
        """ Creating left box """
        pygame.draw.rect(Surface, button_color2, rect)
        for obj in box_data[2]:
            Surface.blit(obj[0], (rect.topleft[0], rect.topleft[1] + obj[1]))
            obj[1] += speed
            check_end(obj, 2)
        """ Creating right box """
        rect.left = rect.right
        pygame.draw.rect(Surface, button_color, rect)
        for obj in box_data[3]:
            Surface.blit(obj[0], (rect.topleft[0], rect.topleft[1] + obj[1]))
            obj[1] += speed
            check_end(obj, 3)
        pygame.draw.line(Surface, Black, rect.topleft, rect.bottomleft)
    else:
        """ Creating right box """
        pygame.draw.rect(Surface, button_color, rect)
        for obj in box_data[3]:
            Surface.blit(obj[0], (rect.topleft[0], rect.topleft[1] + obj[1]))
            obj[1] += speed
            check_end(obj, 3)
        """ Creating left box """
        rect.right = rect.left
        pygame.draw.rect(Surface, button_color2, rect)
        for obj in box_data[2]:
            Surface.blit(obj[0], (rect.topleft[0], rect.topleft[1] + obj[1]))
            obj[1] += speed
            check_end(obj, 2)
        pygame.draw.line(Surface, Black, rect.topright, rect.bottomright)
    """ Drawing boundary if toggle is active"""
    if toggle:
        getrect(3*bar_width, bar_length, center_rect.topleft[0], center_rect.topleft[1], Lightblue, border=border,
                alignment='bottomleft')

    """ Drawing and simulating Bottom Rectangle """
    rect.midtop = center_rect.midbottom
    if gamestate[3]:
        """ Drawing right box """
        pygame.draw.rect(Surface, button_color2, rect)
        for obj in box_data[6]:
            Surface.blit(obj[0], (rect.bottomright[0] - bar_width, rect.bottomright[1] - bar_width - obj[1]))
            obj[1] += speed
            check_end(obj, 6)
        """ Drawing left box """
        rect.right = rect.left
        pygame.draw.rect(Surface, button_color, rect)
        for obj in box_data[7]:
            Surface.blit(obj[0], (rect.bottomright[0] - bar_width, rect.bottomright[1] - bar_width - obj[1]))
            obj[1] += speed
            check_end(obj, 7)
        pygame.draw.line(Surface, Black, rect.topright, rect.bottomright)
    else:
        """ Drawing left box """
        pygame.draw.rect(Surface, button_color, rect)
        for obj in box_data[7]:
            Surface.blit(obj[0], (rect.bottomright[0] - bar_width, rect.bottomright[1] - bar_width - obj[1]))
            obj[1] += speed
            check_end(obj, 7)
        """ Drawing right box """
        rect.left = rect.right
        pygame.draw.rect(Surface, button_color2, rect)
        for obj in box_data[6]:
            Surface.blit(obj[0], (rect.bottomright[0] - bar_width, rect.bottomright[1] - bar_width - obj[1]))
            obj[1] += speed
            check_end(obj, 6)
        pygame.draw.line(Surface, Black, rect.topleft, rect.bottomleft)
    """ Drawing boundary if toggle is inactive """
    if not toggle:
        getrect(3*bar_width, bar_length, center_rect.bottomleft[0], center_rect.bottomleft[1], Lightblue, border=border,
                alignment='topleft')

    getrect(3*bar_width, 3*bar_width, Display_size[0]/2, Display_size[1]/2, border_color, border=border)
    pygame.display.update()


if __name__ == '__main__':
    main()